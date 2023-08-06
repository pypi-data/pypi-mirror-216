/* The mean wall filter, which removes the mean of data along the slow time.
*/


template <typename T>
__device__ void core_mean_wall_filter(T *data,
                                      const int dim_slow_time,
                                      const int nb_pixels,
                                      const bool on_first_axis,
                                      const int i)
{
    /* Definition of the "mean wall filter" function, applies a 'mean' wall
       filter along the slow time axis on IQs. It removes the mean of data
       along the slow time. The input array should be (some dim, ...,
       slow_time_dim) for the regular kernel (working on last axis), or
       (slow_time_dim dim, ..., some) for the transposed kernel, where the slow
       time is assumed to be in the first axis. This only works on pycuda
       complex types, since it is for IQs in Doppler. Other types could be
       implemented though.

      Input parameters:
      =================

      data:          The IQs to clutter-filter.

      dim_slow_time: The packet-size (number of frames along slow time).

      nb_pixels:     The number of pixels in the data array (product of all the
                     dimensions but the slow-time's one).

      on_first_axis: If True, acts on first axis (expects data of shape
                     (slow_time_dim dim, ..., some)). Else case, it should be
                     on last axis (aims to become the default -sole- option).

      i:             The current index of the data (depends on the current
                     thread / block), has been defined in the global caller.
    */
    T mean (0);
    for (int f = 0; f < dim_slow_time; f++) {
        int idx = on_first_axis ? i + f * nb_pixels : i * dim_slow_time + f;
        mean += data[idx];
    }
    mean /= dim_slow_time;
    for (int f = 0; f < dim_slow_time; f++) {
        int idx = on_first_axis ? i + f * nb_pixels : i * dim_slow_time + f;
        data[idx] -= mean;
    }
}


extern "C" {
    __global__ void mean_wall_filter(complex<float> *data,
                                     const int dim_slow_time,
                                     const int nb_pixels)
    {
        /* Caller of the "mean wall filter" function, more information in its
           device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_mean_wall_filter(data, dim_slow_time, nb_pixels, false, i);
        }
    }

    __global__ void mean_wall_filter_first_axis(complex<float> *data,
                                          const int dim_slow_time,
                                          const int nb_pixels)
    {
        /* Caller of the "mean wall filter first axis" function, more
           information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_mean_wall_filter(data, dim_slow_time, nb_pixels, true, i);
        }
    }
}
