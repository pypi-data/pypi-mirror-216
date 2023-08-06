/* Compute the power doppler values from IQs.
*/


template <typename T>
__device__ void core_power_map(const T *data,
                               float *power_map,
                               const int dim_slow_time,
                               const int i)
{
    /* Compute the power map values which is simply the squared data, averaged
       along the slow time (last axis). Note that the real power map then needs
       to be exposed as decibels (using 20 * log10()), which isn't done here.

      Input parameters:
      =================

      color_map:        The array where to store the resulting auto-correlation.

      nyquist_velocity: The nyquist (maximum observable) velocity.

      i:                The current index of the data (depends on the current
                        thread / block), has been defined in the global caller.
    */
    power_map[i] = 0;
    for (int f = 0; f < dim_slow_time; f++) {
        power_map[i] += powf(abs(data[i * dim_slow_time + f]), 2);
    }
    power_map[i] /= float(dim_slow_time);
}


extern "C" {
    __global__ void power_map(const complex<float> *data, float *power_map,
                              const int dim_slow_time, const int nb_pixels)
    {
        /* Caller of the "power map" function, more information in its device
           definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_power_map(data, power_map, dim_slow_time, i);
        }
    }
}
