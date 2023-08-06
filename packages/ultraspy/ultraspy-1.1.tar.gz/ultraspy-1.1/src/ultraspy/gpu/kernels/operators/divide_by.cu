/* Simple divide by float kernel, just divides every elements of an array by a
   given float. It is flexible to float and pycuda complex types.
*/


template <typename T>
__device__ void core_divide_by(T* data,
                               float value,
                               const int i)
{
    /* Definition of the "divide by _" operator, simply divides all the element
       of the data array by a float value.

      Input parameters:
      =================

      data:  The array of the data to divide by value.

      value: The float value to divide by.

      i:     The current index of the data (depends on the current thread /
             block), has been defined in the global caller.
    */
    data[i] /= T(value);
}


extern "C" {
    __global__ void divide_by_float(float *data, float value,
                                    const int nb_points) {
        /* Caller of the "divide by" operator, more information in its device
           definition, given the input data is of type float32.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points) {
            core_divide_by(data, value, i);
        }
    }

    __global__ void divide_by_complex(complex<float> *data, float value,
                                      const int nb_points) {
        /* Caller of the "divide by" operator, more information in its device
           definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points) {
            core_divide_by(data, value, i);
        }
    }
}
