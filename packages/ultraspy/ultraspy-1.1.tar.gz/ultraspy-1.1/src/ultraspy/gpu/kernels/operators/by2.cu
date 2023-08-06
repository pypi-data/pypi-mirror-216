/* Simple by 2 kernel, just multiplies every elements of an array by 2. It is
   flexible to int / float and pycuda complex types.
*/


template <typename T>
__device__ void core_by2(T* data,
                         const int i)
{
    /* Definition of the "by 2" operator, simply multiplies all the element of
       the data array by 2.

      Input parameters:
      =================

      data: The array of the data to multiply by 2.

      i:    The current index of the data (depends on the current thread /
            block), has been defined in the global caller.
    */
    data[i] *= T(2);
}

extern "C" {
    __global__ void by2_int(int *data, const int nb_points) {
        /* Caller of the "by 2" operator, more information in its device
           definition, given the input data is of type int32.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points)
            core_by2(data, i);
    }

    __global__ void by2_float(float *data, const int nb_points) {
        /* Caller of the "by 2" operator, more information in its device
           definition, given the input data is of type float32.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points)
            core_by2(data, i);
    }

    __global__ void by2_complex(complex<float> *data,
                                const int nb_points) {
        /* Caller of the "by 2" operator, more information in its device
           definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points)
            core_by2(data, i);
    }
}
