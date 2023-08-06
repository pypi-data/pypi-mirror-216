/* The kernel to compute the correlation matrix that will be used for color
doppler.
*/


template <typename T>
__device__ void core_correlation_matrix(T *data,
                                        T *color_map,
                                        const int dim_slow_time,
                                        const int nb_pixels,
                                        const int i)
{
    /* Definition of the "correlation matrix" function, for Color Doppler. It
       is performed along last dimension (slow time), with a gap = 1. This only
       works on pycuda complex types, since it is for IQs in Doppler. Other
       types could be implemented though.

      Input parameters:
      =================

      data:          The IQs to auto-correlate for Color Doppler.

      color_map:     The array where to store the resulting auto-correlation.

      dim_slow_time: The packet-size (number of frames along slow time).

      nb_pixels:     The number of pixels in the data array (product of all the
                     dimensions but the slow-time's one).

      i:             The current index of the data (depends on the current
                     thread / block), has been defined in the global caller.
    */
    color_map[i] = 0;
    for (int f = 0; f < dim_slow_time; f++) {
        int idx (i * dim_slow_time + f);
        if (f < dim_slow_time - 1) {
            int idx1 (i * dim_slow_time + (f + 1));
            color_map[i] += data[idx] * conj(data[idx1]);
        }
    }
}


extern "C" {
    __global__ void correlation_matrix(complex<float> *data,
                                       complex<float> *color_map,
                                       const int dim_slow_time,
                                       const int nb_pixels) {
        /* Caller of the "correlation matrix" function, more information in its
           device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_correlation_matrix(data, color_map,
                                    dim_slow_time, nb_pixels, i);
        }
    }
}
