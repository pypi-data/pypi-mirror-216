/* Flip kernel, which flips the data within the first axis of a 2d array. It is
flexible to int / float and pycuda complex types. It is also flexible to a
larger array with a higher number of dimensions as long as the given number of
points in the axis 2 is adapted (dim_axis2 -> product of the points in axes 2,
3, ...). Note that there is also a second version (flip_old), which weirdly
works along the last axis on wrongly sized array... It's still here since it
still is the one used in filtfilt (TODO).
*/


template <typename T>
__device__ void core_flip(const T* data,
                          T* flipped_data,
                          const int dim_axis1,
                          const int dim_axis2,
                          const int i)
{
    /* Definition of the "flip" operator, which flips the data within the first
       axis of a 2d array. It is also flexible to a larger array with a higher
       number of dimensions as long as the given number of points in the axis 2
       is adapted (dim_axis2 -> product of the points in axes 2, 3, ...).

      Input parameters:
      =================

      data:         The array of the data to flip, along the last axis,
                    somehow.

      flipped_data: The flipped array where to store the resulting array.

      dim_axis1:    The number of elements in the first axis.

      dim_axis2:    The number of elements in the last axis. Note that if data
                    is not 2D, dim_axis2 is the product of all the dimensions
                    (but the first one, the one on which to operate).

      i:            The current index of the data (depends on the current
                    thread / block), has been defined in the global caller.
    */
    int idx_row = (int)i / dim_axis2;
    int idx_col = (int)i % dim_axis2;
    int rev_idx_row = dim_axis1 - 1 - idx_row;
    int rev_i = rev_idx_row * dim_axis2 + idx_col;
    if (rev_idx_row > idx_row) {
        T tmp = data[i];
        flipped_data[i] = data[rev_i];
        flipped_data[rev_i] = tmp;
    }
}


template <typename T>
__device__ void core_flip_old(const T* data,
                              T* flipped_data,
                              const int dim_axis1,
                              const int i)
{
    /* Definition of the old "flip" operator, it is weirdly working along the
       last axis on wrongly sized array... It's still here since it still is
       the one used in filtfilt, for now.

      Input parameters:
      =================

      data:         The array of the data to flip, along the last axis,
                    somehow.

      flipped_data: The flipped array where to store the resulting array.

      dim_axis1:    The number of elements in the first axis. Note that if data
                    is not 2D, dim_axis1 is the product of all the dimensions
                    (but the last one, the one on which to operate).

      i:            The current index of the data (depends on the current
                    thread / block), has been defined in the global caller.
    */
    int idx_axis2 = int(i / dim_axis1) * dim_axis1;
    int it = i - idx_axis2;
    if (it < (dim_axis1 / 2) + 1) {
        T tmp = data[i];
        flipped_data[i] = data[idx_axis2 + dim_axis1 - 1 - it];
        flipped_data[idx_axis2 + dim_axis1 - 1 - it] = tmp;
    }
}


extern "C" {
    __global__ void flip_int(int *data, const int dim_axis1,
                             const int dim_axis2) {
        /* Caller of the "flip" operator, more information in its device
           definition, given the input data is of type int32.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip(data, data, dim_axis1, dim_axis2, i);
    }

    __global__ void flip_float(float *data, const int dim_axis1,
                               const int dim_axis2) {
        /* Caller of the "flip" operator, more information in its device
           definition, given the input data is of type float32.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip(data, data, dim_axis1, dim_axis2, i);
    }

    __global__ void flip_complex(complex<float> *data, const int dim_axis1,
                                 const int dim_axis2) {
        /* Caller of the "flip" operator, more information in its device
           definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip(data, data, dim_axis1, dim_axis2, i);
    }

    __global__ void flip_within_int(const int *data, int *flipped_data,
                                    const int dim_axis1,
                                    const int dim_axis2) {
        /* Caller of the "flip within" operator, more information in its device
           definition, given the input data is of type int32. The 'within' variant
           is storing the resulting array within another array (not in place).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip(data, flipped_data, dim_axis1, dim_axis2, i);
    }

    __global__ void flip_within_float(const float *data, float *flipped_data,
                                      const int dim_axis1,
                                      const int dim_axis2) {
        /* Caller of the "flip within" operator, more information in its device
           definition, given the input data is of type float32. The 'within'
           variant is storing the resulting array within another array (not in
           place).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip(data, flipped_data, dim_axis1, dim_axis2, i);
    }

    __global__ void flip_within_complex(const complex<float> *data,
                                        complex<float> *flipped_data,
                                        const int dim_axis1,
                                        const int dim_axis2) {
        /* Caller of the "flip within" operator, more information in its device
           definition, given the input data is of type complex<float>.
           The 'within' variant is storing the resulting array within another
           array (not in place).
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip(data, flipped_data, dim_axis1, dim_axis2, i);
    }


    // Last axis alternative, used in signals, might be deprecated after
    // investigation
    __global__ void flip_old_complex(complex<float> *data, const int dim_axis1,
                                     const int dim_axis2) {
        /* Caller of the "flip old" operator, more information in its device
           definition, given the input data is of type complex<float>.
           Might be deprecated after investigation.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip_old(data, data, dim_axis1, i);
    }

    __global__ void flip_within_old_complex(complex<float> *data,
                                            complex<float> *flipped_data,
                                            const int dim_axis1,
                                            const int dim_axis2) {
        /* Caller of the "flip within old" operator, more information in its
           device definition, given the input data is of type complex<float>.
           The 'within' variant is storing the resulting array within another
           array (not in place). Might be deprecated after investigation.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < dim_axis1 * dim_axis2)
            core_flip_old(data, flipped_data, dim_axis1, i);
    }
}
