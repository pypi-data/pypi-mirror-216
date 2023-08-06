/* Down-mixing operation. Centers the spectrum of our data at 0 Hz. It
considers the time samples are in the last dimension.
*/

#define M_PI 3.14159265358979323846


__device__ void core_down_mix(complex<float> *data,
                              const int dim_time_samples,
                              const float t0,
                              const float central_freq,
                              const float sampling_freq,
                              const int i)
{
    /* Definition of the "down mix" function, which centers the spectrum of
       frequencies of our signal at 0 Hz. The resulting signal is then, by
       definition, complex.

      Input parameters:
      =================

      data:             The array of the data to down-mix, the operation is
                        inplace, so the data should already be of a complex
                        type. The time samples should be the last dimension.

      dim_time_samples: The number of samples along the time sample axis (last
                        dimension).

      t0:               The initial time the signal has been recorded.

      central_freq:     The central frequency of the probe.

      sampling_freq:    The sampling frequency of the acquisition.

      i:                The current index of the data (depends on the current
                        thread / block), has been defined in the global caller.
    */
    int it = (int)i % dim_time_samples;
    float w = -2.0f * M_PI * central_freq * (t0 + it / float(sampling_freq));
    complex<float> phase (cosf(w), sinf(w));
    data[i] *= phase;
}


extern "C" {
    __global__ void down_mix(complex<float> *data, const int dim_time_samples,
                             const int nb_data, const float t0,
                             const float central_freq,
                             const float sampling_freq) {
        /* Caller of the "down mix" function, more information in its device
           definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_time_samples * nb_data) {
            core_down_mix(data, dim_time_samples, t0,
                          central_freq, sampling_freq, i);
        }
    }
}
