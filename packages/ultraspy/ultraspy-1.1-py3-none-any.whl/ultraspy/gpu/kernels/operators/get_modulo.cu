/* Get the modulo of complex signals and stores it in another array (of type
float).
*/


__device__ void core_get_modulo(const complex<float> *data,
                                float *envelope,
                                const int i)
{
    /* Definition of the "get modulo" operator, simply returns the modulo of
       all the element of the complex data array.

      Input parameters:
      =================

      data:     The array of the original data (of type complex).

      envelope: The returned array, with the modulo of the data (of type
                float32).

      i:        The current index of the data (depends on the current thread /
                block), has been defined in the global caller.
    */
    envelope[i] = abs(data[i]);
}


extern "C" {
    __global__ void get_modulo(const complex<float> *data, const int nb_points,
                               float *envelope) {
        /* Caller of the "get modulo" operator, more information in its device
           definition, given the input data is of type complex<float>.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_points) {
            core_get_modulo(data, envelope, i);
        }
    }
}
