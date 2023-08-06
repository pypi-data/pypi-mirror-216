/* Compute the doppler velocity from a previously computed correlation matrix.
*/

#define M_PI 3.14159265358979323846


template <typename T>
__device__ void core_color_map(T *color_map,
                               const float nyquist_velocity,
                               const int i)
{
    /* Compute the doppler velocity from a previously computed correlation
       matrix. The formula is -v_c * Imag(log(data)) / pi. Note that the
       modified color map is of a complex type, even though we've selected its
       imaginary part. Therefore it can be converted to float using
       gpu_array_color_map.real.astype(np.float32) from host.

      Input parameters:
      =================

      color_map:        The array where to store the resulting auto-correlation.

      nyquist_velocity: The nyquist (maximum observable) velocity.

      i:                The current index of the data (depends on the current
                        thread / block), has been defined in the global caller.
    */
    color_map[i] = -nyquist_velocity * log(color_map[i]).imag() / M_PI;
}


extern "C" {
    __global__ void color_map(complex<float> *color_map,
                              const float nyquist_velocity,
                              const int nb_pixels) {
        /* Caller of the "color map" function, more information in its device
           definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_color_map(color_map, nyquist_velocity, i);
        }
    }
}
