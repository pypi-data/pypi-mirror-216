/* To decibel kernel, which simply returns the data to 20 * log10(data). It is
only flexible to float type.
*/


template <typename T>
__device__ void core_to_db(T* data,
                           const bool power,
                           const int i)
{
    /* Definition of the "to dB" operator, simply returns 20 * log10(data) for
       all the element of the input data array.

      Input parameters:
      =================

      data:  The array of the original data.

      power: If True, we are converting power data.

      i:     The current index of the data (depends on the current thread /
             block), has been defined in the global caller.
    */
    if (power) {
        data[i] = 10 * log10(data[i]);
    } else {
        data[i] = 20 * log10(data[i]);
    }
}


extern "C" {
    __global__ void to_db_float(float *data, int nb_points) {
        /* Caller of the "to dB" operator, more information in its device
           definition, given the input data is of type float.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points)
            core_to_db(data, false, i);
    }

    __global__ void power_to_db_float(float *data, int nb_points) {
        /* Caller of the "to dB" operator, more information in its device
           definition, given the input data is of type float.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points)
            core_to_db(data, true, i);
    }
}
