/* Two main kernels here 1) Convolution for 1D (cross-correlation) and 2)
Convolution for 2D arrays
Both are flexible to float and pycuda complex types. Convolve1d can be applied
on arrays of extended shape, the convolution will just be performed along the
first dimension. However, Convolve2d will leads to errors if our array has more
dimensions than 2.
TODO: Maybe it is not the most efficient way..? This one is very
      straightforward, might worth to check some algorithms if it turns out too
      slow
*/


template <typename T>
__device__ void core_convolve1d(const T* data,
                                T *convolved_data,
                                const float *kernel,
                                const int dim_axis2,
                                const int kernel_size,
                                const int i)
{
    /* Definition of the "convolve 1d" operator, performs a 1D convolution
       given a convolution vector (kernel) on the first axis of our data. It is
       assuming zero padding at borders.

      Input parameters:
      =================

      data:           The array of the original data.

      convolved_data: The array to modify, with the convolved data.

      kernel:         The vector convolution kernel.

      dim_axis2:      The number of elements in the second dimension.

      kernel_size:    The size of the kernel.

      i:              The current index of the data (depends on the current
                      thread / block), has been defined in the global caller.
    */
    int gap = (int)kernel_size / 2;
    int idx_i = (int)i / dim_axis2;
    int idx_j = (int)i % dim_axis2;
    convolved_data[i] = T(0);

    for (int k_j = -gap; k_j <= gap; k_j++) {
        if (idx_j + k_j >= 0 && idx_j + k_j < dim_axis2) {
            float w = kernel[k_j + gap];
            convolved_data[i] += w * data[(idx_i * dim_axis2) + (idx_j + k_j)];
        }
    }
}


template <typename T>
__device__ void core_convolve2d(const T* data,
                                T *convolved_data,
                                const float *kernel,
                                const int dim_data_x,
                                const int dim_data_y,
                                const int kernel_size,
                                const int i)
{
    /* Definition of the "convolve 2d" operator, the convolution matrix
       (kernel) is applied to each pixel of our 2D array, using a 'same' method
       at borders. The kernel must be a square. Note that it provides the same
       results as the typical Python CPU equivalent for kernels with odd shapes
       (1x1, 3x3, 5x5, ..), so those should be preferred.

      Input parameters:
      =================

      data:           The array of the original data.

      convolved_data: The array to modify, with the convolved data.

      kernel:         The squared convolution kernel. It is preferred to use
                      odd shapes so the kernels are rightly centered for every
                      pixel.

      dim_data_x:     The number of elements in the first dimension.

      dim_data_y:     The number of elements in the second dimension.

      kernel_size:    The size of the squared kernel (preferentially odd).

      i:              The current index of the data (depends on the current
                      thread / block), has been defined in the global caller.
    */
    int gap = (int)kernel_size / 2;
    int centered_idx_i = (int)i / dim_data_y;
    int centered_idx_j = (int)i % dim_data_y;
    convolved_data[i] = T(0);

    for (int k_i = -gap; k_i <= gap; k_i++) {
        for (int k_j = -gap; k_j <= gap; k_j++) {
            float w = kernel[(k_i + gap) * kernel_size + (k_j + gap)];
            int idx_i = centered_idx_i + k_i;
            int idx_j = centered_idx_j + k_j;
            if (idx_i < 0) { idx_i = 0; }
            if (idx_i >= dim_data_x) { idx_i = dim_data_x - 1; }
            if (idx_j < 0) { idx_j = 0; }
            if (idx_j >= dim_data_y) { idx_j = dim_data_y - 1; }

            convolved_data[i] += w * data[idx_i * dim_data_y + idx_j];
        }
    }
}


extern "C" {
    __global__ void convolve1d_float(const float *data, float *convolved_data,
                                     const float *kernel, const int dim_axis1,
                                     const int dim_axis2,
                                     const int kernel_size) {
        /* Caller of the "convolve 1d" operator, more information in its device
           definition, given the input data is of type float.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2) {
            core_convolve1d(data, convolved_data, kernel, dim_axis2,
                            kernel_size, i);
        }
    }

    __global__ void convolve1d_complex(const complex<float> *data,
                                       complex<float> *convolved_data,
                                       const float *kernel,
                                       const int dim_axis1,
                                       const int dim_axis2,
                                       const int kernel_size) {
        /* Caller of the "convolve 1d" operator, more information in its device
           definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2) {
            core_convolve1d(data, convolved_data, kernel, dim_axis2,
                            kernel_size, i);
        }
    }

    __global__ void convolve2d_float(const float *data, float *convolved_data,
                                     const float *kernel, const int dim_data_x,
                                     const int dim_data_y,
                                     const int kernel_size) {
        /* Caller of the "convolve 2d" operator, more information in its device
           definition, given the input data is of type float.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_data_x * dim_data_y) {
            core_convolve2d(data, convolved_data, kernel, dim_data_x,
                            dim_data_y, kernel_size, i);
        }
    }

    __global__ void convolve2d_complex(const complex<float> *data,
                                       complex<float> *convolved_data,
                                       const float *kernel,
                                       const int dim_data_x,
                                       const int dim_data_y,
                                       const int kernel_size) {
        /* Caller of the "convolve 2d" operator, more information in its device
           definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_data_x * dim_data_y) {
            core_convolve2d(data, convolved_data, kernel, dim_data_x,
                            dim_data_y, kernel_size, i);
        }
    }
}
