/* Kernels for the median filter, on float or complex (for the latter, performs
separately the median filters on both real / imaginary components).
TODO: Maybe it is not the most efficient way..? This one is very
      straightforward, might worth to check some algorithms if it turns out too
      slow
*/


template <typename T>
__device__ void core_median_filter(const T* data,
                                   T *filtered_data,
                                   const int dim_data_x,
                                   const int dim_data_y,
                                   const int kernel_size,
                                   const int i)
{
    /* Definition of the median filter on 2d data, the filter is squared,
       defined with kernel_size, and applied to each pixel of our 2D array,
       using a 'same' method at borders. Note that it provides the same
       results as the typical Python CPU equivalent for kernels with odd shapes
       (1x1, 3x3, 5x5, ..), so those should be preferred.

      Input parameters:
      =================

      data:          The array of the original data.

      filtered_data: The array to modify, with the convolved data.

      dim_data_x:    The number of elements in the first dimension.

      dim_data_y:    The number of elements in the second dimension.

      kernel_size:   The size of the squared kernel (preferentially odd).

      i:             The current index of the data (depends on the current
                     thread / block), has been defined in the global caller.
    */
    int gap = (int)kernel_size / 2;
    int centered_idx_i = (int)i / dim_data_y;
    int centered_idx_j = (int)i % dim_data_y;
    filtered_data[i] = T(0);

    for (int k_i = -gap; k_i <= gap; k_i++) {
        for (int k_j = -gap; k_j <= gap; k_j++) {
            int idx_i = centered_idx_i + k_i;
            int idx_j = centered_idx_j + k_j;
            if (idx_i < 0) { idx_i = 0; }
            if (idx_i >= dim_data_x) { idx_i = dim_data_x - 1; }
            if (idx_j < 0) { idx_j = 0; }
            if (idx_j >= dim_data_y) { idx_j = dim_data_y - 1; }

            filtered_data[i] = 0;
        }
    }
}


extern "C" {
    __global__ void median_filter_float(const float *data, float *filtered_data,
                                        const int dim_data_x,
                                        const int dim_data_y,
                                        const int kernel_size) {
        /* Caller of the "median filter" operator, more information in its
           device definition, given the input data is of type float.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_data_x * dim_data_y) {
            core_median_filter(data, filtered_data, dim_data_x, dim_data_y,
                               kernel_size, i);
        }
    }

    __global__ void median_filter_complex(const complex<float> *data,
                                          complex<float> *filtered_data,
                                          const int dim_data_x,
                                          const int dim_data_y,
                                          const int kernel_size) {
        /* Caller of the "median filter" operator, more information in its
           device definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_data_x * dim_data_y) {
            core_median_filter(data, filtered_data, dim_data_x, dim_data_y,
                               kernel_size, i);
        }
    }
}
