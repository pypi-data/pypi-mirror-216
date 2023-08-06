/* Initialization process that needs to be perform before a filtfilt operation.
Given that we want to filter some data of shape (nb_x, nb_z) along the last
axis, we need the temporary arrays:
- input_dx (nb_x, nb_ext)
- output_dz (nb_x, order + 1)
(with order the filter order, and nb_ext = 3 * (order - 1))
The initialization does...

TODO: Proper documentation.
*/


template <typename T>
__device__ void core_init_filter(const T *input_dx,
                                 T *output_dz,
                                 const float *init_conditions,
                                 const int filter_order,
                                 const int nb_ext,
                                 const int i)
{
    /* Definition of the "init filter" function.
       TODO: Complete

      Input parameters:
      =================

      input_dx:        TODO

      output_dz:       TODO

      init_conditions: TODO

      filter_order:    TODO

      nb_ext:          TODO

      i:               The current index of the data (depends on the current
                       thread / block), has been defined in the global caller.
    */
    int idx_data_x = (int)(i / filter_order);
    int iz = i - idx_data_x * filter_order;

    if (iz == filter_order - 1) {
        output_dz[i] = T(0);
    } else {
        output_dz[i] = init_conditions[iz] * input_dx[idx_data_x * nb_ext];
    }
}


extern "C" {
    __global__ void init_filter_float(const float *input_dx, float *output_dz,
                                      const float *init_conditions,
                                      const int filter_order, const int nb_ext,
                                      const int nb_data) {
        /* Caller of the "init filter" function on float data, more information
           in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < filter_order * nb_data) {
            core_init_filter(input_dx, output_dz, init_conditions,
                             filter_order, nb_ext, i);
        }
    }

    __global__ void init_filter_complex(const complex<float> *input_dx,
                                        complex<float> *output_dz,
                                        const float *init_conditions,
                                        const int filter_order,
                                        const int nb_ext,
                                        const int nb_data) {
        /* Caller of the "init filter" function on complex data, more
           information in its device definition.
        */
        const int i = threadIdx.x + blockDim.x * blockIdx.x;
        if (i < filter_order * nb_data) {
            core_init_filter(input_dx, output_dz, init_conditions,
                             filter_order, nb_ext, i);
        }
    }
}
