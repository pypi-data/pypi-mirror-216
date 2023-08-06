/* Actual DAS kernel. A few options are available:
- interpolation: 0 or 1 (none or linear)
- should_average: 0 or 1 (False or True)
- rx_apodization_method: 0 or 1 (Boxcar or Tukey window)
- rx_apodization_alpha: Factor (float) for our apodization window
- emitted_aperture: If True, the aperture is computed for emission elements
  also
- compound: If True, the data is compounded through the transmissions
- reduce: If True, the data is reduced through the probe elements
*/

#define M_PI 3.14159265358979323846

#include "probe_distances.cu"
#include "aperture_ratio.cu"
#include "interpolation.cu"
#include "apodization.cu"


template <class T>
__device__ void core_das(const T *data,
                         const int start_data_idx,
                         const int is_iq,
                         const float *emitted_probe,
                         const float *received_probe,
                         const float *emitted_thetas,
                         const float *received_thetas,
                         const float *delays,
                         const int nb_t,
                         const int nb_ee,
                         const int nb_re,
                         const int nb_ts,
                         const float sampling_freq,
                         const float central_freq,
                         const float t0,
                         const float sound_speed,
                         const float *f_number,
                         const float x,
                         const float y,
                         const float z,
                         complex<float> *grid,
                         const int nb_pixels,
                         const int interpolation_method,
                         const int should_average,
                         const int rx_apodization_method,
                         const float rx_apodization_alpha,
                         const int emitted_aperture,
                         const int compound,
                         const int reduce,
                         const int i)
{
    /* Delay And Sum algorithm kernel, called in parallel for each pixel. It
       does, for each transmission:
        - computes the distances between the pixel to beamform and the probe /
          distance in the meridional plane, to get the aperture ratios. If it
          is not visible by the probe element, it is skipped.
        - computes the transmissions distances, as the closest probe element to
          each pixel
        - for each element of the received probe, computes the reception
          distance. If needed, a phase rotation is performed (for I/Qs) and,
          then, we get the corresponding interpolated data
        - average if required

      Input parameters:
      =================

      data:                  The RFs to beamform, of shape (nb_a, nb_e, nb_t).

      start_data_idx:        The index of the first data to consider (if we are
                             working on a packet, this tells us from where to
                             expect to find the related frame).

      is_iq:                 Is set to 1 if the data are I/Qs (thus a phase
                             rotation is required).

      emitted_probe:         The positions of the elements of the emission
                             probe (three dimensional).

      received_probe:        The positions of the elements of the reception
                             probe (three dimensional).

      emitted_thetas:        The thetas of the emission probe (per cycle).

      received_thetas:       The thetas of the reception probe (per cycle).

      delays:                The array with all the delays of our emission
                             sequences.

      nb_t:                  The number of transmissions in our data.

      nb_ee:                 The number of emitted elements in the probe.

      nb_re:                 The number of received elements in the probe.

      nb_ts:                 The number of time samples.

      sampling_freq:         The sampling frequency of the acquisition.

      central_freq:          The central frequency of the probe used for the
                             acquisition.

      t0:                    The initial time of recording.

      sound_speed:           The speed of sound of the scanned medium.

      f_number:              The aperture of the probe elements. For any
                             position of the medium, (z / f_number)-width
                             elements of the probe may have an aperture wide
                             enough to observe at depth z. Two-dimensional, for
                             both the lateral and elevational axes.

      x:                     The x position of the current pixel.

      y:                     The y position of the current pixel.

      z:                     The z position of the current pixel.

      grid:                  The grid where to store the beamformed results.

      nb_pixels:             The number of pixels in the grid.

      interpolation_method:  The interpolation method to use (can be 0 (no
                             interpolation) or 1 (linear)).

      should_average:        This option defines if we average the results
                             after beamforming (by the number of locally
                             concerned elements, check f_number for details).
                             If 1, Delay And Mean is performed, else cas, Delay
                             And Sum.

      rx_apodization_method: The apodization method at reception to apply (can
                             be either 0 (boxcar) or 1 (tukey)).

      rx_apodization_alpha:  The coefficient to provide to our apodization
                             window (if 0, no apodization).

      emitted_aperture:      Set to 1 if the emitted elements have an aperture,
                             else case, 0.

      compound:              If set to 0, will not compound along the
                             transmissions.

      reduce:                If set to 0, will not reduce along the probe
                             elements.

      i:                     The current index of the data (depends on the
                             current thread / block), has been defined in the
                             global caller.
    */
    int dim_nb_t = compound == 1 ? 1 : nb_t;
    int dim_nb_re = reduce == 1 ? 1 : nb_re;

    int count_t = 0;
    for (int it = 0; it < nb_t; it++) {
        int base_it = it * dim_nb_re * nb_pixels;

        float transmission = 10;  // 10m for infinity
        for (int iee = 0; iee < nb_ee; iee++) {
            float e_dist_to_x, e_dist_to_y, e_dists;
            get_distances(emitted_probe, nb_t, nb_ee, it, iee, x, y, z,
                          &e_dist_to_x, &e_dist_to_y, &e_dists);

            int base = it * nb_ee + iee;
            if (emitted_aperture == 1) {
                float e_ratio = get_aperture_ratio(
                    z, e_dist_to_x, e_dist_to_y, e_dists,
                    emitted_thetas[base], f_number);
                if (abs(e_ratio) > 1) {
                    continue;
                }
            }

            transmission = min(transmission,
                               delays[base] * sound_speed + e_dists);
        }

        if (transmission >= 10) {
            continue;
        }

        int count_re = 0;
        for (int ire = 0; ire < nb_re; ire++) {
            int base_ire = ire * nb_pixels;

            float r_dist_to_x, r_dist_to_y, r_dists;
            get_distances(received_probe, nb_t, nb_re, it, ire, x, y, z,
                          &r_dist_to_x, &r_dist_to_y, &r_dists);

            int base = it * nb_re + ire;
            float r_ratio = get_aperture_ratio(
                z, r_dist_to_x, r_dist_to_y, r_dists,
                received_thetas[base], f_number);

            if (abs(r_ratio) > 1) {
                continue;
            }

            float reception = r_dists;
            float tau = (reception + transmission) / sound_speed;
            float delay = tau - t0;
            float data_idx = delay * sampling_freq;

            // Get the corresponding data
            int base_idx = start_data_idx + it * nb_re * nb_ts + ire * nb_ts;
            complex<float> focused_data = interpolate(
                data, base_idx, data_idx, nb_ts, interpolation_method);

            if (focused_data != T(0)) {
                count_re++;

                // Default to 1 for the apodization method here
                focused_data *= get_apodization_weight(
                    r_ratio, rx_apodization_alpha, rx_apodization_method);

                if (is_iq == 1) {
                    // Phase rotation for IQs (does nothing if data are RFs)
                    complex<float> phase (0, 2 * M_PI * central_freq * tau);
                    focused_data *= exp(phase);
                }

                // Add it to the grid
                int real_i = i;
                if (compound == 0) { real_i += base_it; }
                if (reduce == 0) { real_i += base_ire; }
                grid[real_i] += focused_data;
            }
        }
        if (compound == 1 && reduce == 1) {
            count_t += count_re;
        } else if (compound == 0 && reduce == 1) {
            if (should_average == 1 && count_re > 0) {
                grid[i + base_it] /= count_re;
            }
        } else if (compound == 1 && reduce == 0) {
            count_t += count_re > 0 ? 1 : 0;
        }
        count_re = 0;
    }

    if (should_average == 1 && count_t > 0 && compound == 1) {
        for (int it = 0; it < dim_nb_t; it++) {
            for (int ire = 0; ire < dim_nb_re; ire++) {
                int base_i = it * dim_nb_re * nb_pixels + ire * nb_pixels;
                grid[base_i + i] /= T(count_t);
            }
        }
    }
}


extern "C" {
    __global__ void das_float(
            const float *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_t, const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *grid, const int nb_pixels,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "das" beamformer, more information in its device
           definition. It is expecting RFs (data of float type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * nb_pixels);
            int i_in_elements = (int)i_in_transmission % nb_pixels;
            int idx_p = (int)i_in_elements % nb_pixels;

            core_das(data, 0, is_iq, emitted_probe, received_probe,
                     emitted_thetas, received_thetas, delays,
                     nb_t, nb_ee, nb_re, nb_ts,
                     sampling_freq, central_freq, t0, sound_speed, f_number,
                     x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                     grid, nb_pixels,
                     interpolation_method, should_average,
                     rx_apodization_method, rx_apodization_alpha,
                     emitted_aperture, compound, reduce, i);
        }
    }

    __global__ void das_complex(
            const complex<float> *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_t, const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *grid, const int nb_pixels,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "das" beamformer, more information in its device
           definition. It is expecting I/Qs (data of complex type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * nb_pixels);
            int i_in_elements = (int)i_in_transmission % nb_pixels;
            int idx_p = (int)i_in_elements % nb_pixels;

            core_das(data, 0, is_iq, emitted_probe, received_probe,
                     emitted_thetas, received_thetas, delays,
                     nb_t, nb_ee, nb_re, nb_ts,
                     sampling_freq, central_freq, t0, sound_speed, f_number,
                     x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                     grid, nb_pixels,
                     interpolation_method, should_average,
                     rx_apodization_method, rx_apodization_alpha,
                     emitted_aperture, compound, reduce, i);
        }
    }

    __global__ void packet_das_float(
            const float *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_f, const int nb_t,
            const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *grid, const int total_nb_pixels,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "das" beamformer working on packet of data, more
           information in its device definition. It is expecting RFs (data of
           float type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < total_nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * total_nb_pixels);
            int i_in_elements = (int)i_in_transmission % total_nb_pixels;
            int i_in_pixels = (int)i_in_elements % nb_f;

            int idx_p = (int)i_in_elements / nb_f;
            int idx_f = i_in_pixels;

            int data_start_idx = idx_f * nb_t * nb_re * nb_ts;

            core_das(data, data_start_idx, is_iq, emitted_probe, received_probe,
                     emitted_thetas, received_thetas, delays,
                     nb_t, nb_ee, nb_re, nb_ts,
                     sampling_freq, central_freq, t0, sound_speed, f_number,
                     x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                     grid, total_nb_pixels,
                     interpolation_method, should_average,
                     rx_apodization_method, rx_apodization_alpha,
                     emitted_aperture, compound, reduce, i);
        }
    }

    __global__ void packet_das_complex(
            const complex<float> *data, const int is_iq,
            const float *emitted_probe, const float *received_probe,
            const float *emitted_thetas, const float *received_thetas,
            const float *delays,
            const int nb_f, const int nb_t,
            const int nb_ee, const int nb_re, const int nb_ts,
            const float sampling_freq, const float central_freq, const float t0,
            const float sound_speed, const float *f_number,
            const float *x_coords, const float *y_coords, const float *z_coords,
            const int dim_nb_t, const int dim_nb_re,
            complex<float> *grid, const int total_nb_pixels,
            const int interpolation_method, const int should_average,
            const int rx_apodization_method, const float rx_apodization_alpha,
            const int emitted_aperture, const int compound, const int reduce)
    {
        /* Caller of the "das" beamformer working on packet of data, more
           information in its device definition. It is expecting I/Qs (data of
           complex type).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < total_nb_pixels) {
            int i_in_transmission = (int)i % (dim_nb_re * total_nb_pixels);
            int i_in_elements = (int)i_in_transmission % total_nb_pixels;
            int i_in_pixels = (int)i_in_elements % nb_f;

            int idx_p = (int)i_in_elements / nb_f;
            int idx_f = i_in_pixels;

            int data_start_idx = idx_f * nb_t * nb_re * nb_ts;

            core_das(data, data_start_idx, is_iq, emitted_probe, received_probe,
                     emitted_thetas, received_thetas, delays,
                     nb_t, nb_ee, nb_re, nb_ts,
                     sampling_freq, central_freq, t0, sound_speed, f_number,
                     x_coords[idx_p], y_coords[idx_p], z_coords[idx_p],
                     grid, total_nb_pixels,
                     interpolation_method, should_average,
                     rx_apodization_method, rx_apodization_alpha,
                     emitted_aperture, compound, reduce, i);
        }
    }
}
