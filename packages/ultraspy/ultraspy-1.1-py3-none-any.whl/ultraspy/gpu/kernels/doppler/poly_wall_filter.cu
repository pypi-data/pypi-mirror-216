/* The polynomial wall filter, which removes the first n degrees of the
polynomial regression along the slow time.
*/


template <typename T>
__device__ void core_poly_wall_filter(T *data,
                                      const float *polys,
                                      const int n,
                                      const int dim_slow_time,
                                      const int nb_pixels,
                                      const bool on_first_axis,
                                      const int i)
{
    /* Definition of the "polynomial wall filter" function, applies a
       'polynomial' wall filter along the slow time axis on IQs. It removes the
       first n degrees of the polynomial regression along the slow time. The
       input array should be (some dim, ..., slow_time_dim) for the regular
       kernel (working on last axis), or (slow_time_dim dim, ..., some) for the
       transposed kernel, where the slow time is assumed to be in the first
       axis. This only works on pycuda complex types, since it is for IQs in
       Doppler. Other types could be implemented though.

      Input parameters:
      =================

      data:          The IQs to clutter-filter.

      polys:         The polynomial coefficients given the degree of the
                     regression.

      n:             The degree for the clutter-filter (dimension of the
                     polynomial regression)

      dim_slow_time: The packet-size (number of frames along slow time).

      nb_pixels:     The number of pixels in the data array (product of all the
                     dimensions but the slow-time's one).

      on_first_axis: If True, acts on first axis (expects data of shape
                     (slow_time_dim dim, ..., some)). Else case, it should be
                     on last axis (aims to become the default -sole- option).

      i:             The current index of the data (depends on the current
                     thread / block), has been defined in the global caller.
    */
    for (int o = 0; o < n + 1; o++) {
        T coefficients = 0;
        T denominator = 0;
        for (int f = 0; f < dim_slow_time; f++) {
            int idx_o = on_first_axis ? f * (n + 1) + o : o * dim_slow_time + f;
            int idx_i = on_first_axis ? f * nb_pixels + i : i * dim_slow_time + f;
            coefficients += polys[idx_o] * data[idx_i];
            denominator += polys[idx_o] * polys[idx_o];
        }
        for (int f = 0; f < dim_slow_time; f++) {
            int idx_o = on_first_axis ? f * (n + 1) + o : o * dim_slow_time + f;
            int idx_i = on_first_axis ? f * nb_pixels + i : i * dim_slow_time + f;
            data[idx_i] -= T(polys[idx_o]) * coefficients / denominator;
        }
    }
}


extern "C" {
    __global__ void poly_wall_filter(complex<float> *data, const float *polys,
                                     const int n, const int dim_slow_time,
                                     const int nb_pixels) {
        /* Caller of the "polynomial wall filter" function, more information in
           its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_poly_wall_filter(data, polys, n, dim_slow_time, nb_pixels,
                                  false, i);
        }
    }

    __global__ void poly_wall_filter_first_axis(complex<float> *data,
                                                const float *polys, const int n,
                                                const int dim_slow_time,
                                                const int nb_pixels) {
        /* Caller of the "polynomial wall filter first axis" function, more
           information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_pixels) {
            core_poly_wall_filter(data, polys, n, dim_slow_time, nb_pixels,
                                  true, i);
        }
    }
}
