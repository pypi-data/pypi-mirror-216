/* Operation between the data to filter (nb_x, nb_z) and tmp_x (nb_x, nb_ext).
It fills the tmp_x array with, for each nb_ext n, the value:
end0 - data[nb_ext - n], with end0 twice the last time sample for a given data.

TODO: Proper documentation.
*/


template <typename T>
__device__ void core_init_end_sig(const T *data,
                                  T *output_dx,
                                  const int nb_ext,
                                  const int dim_time_samples,
                                  const int i)
{
    /* Definition of the "init end signal" function.
       TODO: Complete

      Input parameters:
      =================

      data:             TODO

      output_dz:        TODO

      nb_ext:           TODO

      dim_time_samples: TODO

      i:                The current index of the data (depends on the current
                        thread / block), has been defined in the global caller.
    */
    int idx_data = i * dim_time_samples + dim_time_samples - 1;
    T end0 = 2.0f * data[idx_data];
    for (int it = 0; it < nb_ext; it++) {
        output_dx[i * nb_ext + it] = end0 - data[idx_data - 1 - it];
    }
}


extern "C" {
    __global__ void init_end_sig_float(const float *data, float *output_dx,
                                       const int nb_ext,
                                       const int dim_time_samples,
                                       const int nb_data) {
        /* Caller of the "init end signal" function on float data, more
        information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_data) {
            core_init_end_sig(data, output_dx, nb_ext, dim_time_samples, i);
        }
    }

    __global__ void init_end_sig_complex(const complex<float> *data,
                                         complex<float> *output_dx,
                                         const int nb_ext,
                                         const int dim_time_samples,
                                         const int nb_data) {
        /* Caller of the "init end signal" function on complex data, more
        information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < nb_data) {
            core_init_end_sig(data, output_dx, nb_ext, dim_time_samples, i);
        }
    }
}
