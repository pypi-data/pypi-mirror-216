/* ...

TODO: Proper documentation.
*/


template <typename T>
__device__ void core_filter0(const T *input_dx,
                             T *output_dz,
                             T *tmp_data_dy,
                             const float *dBS,
                             const float *dAS,
                             const int filter_order,
                             const int dim_time_samples,
                             const int i)
{
    /* Definition of the "filter0" function.
       TODO: Complete

      Input parameters:
      =================

      input_dx:         TODO

      output_dz:        TODO

      tmp_data_dy:      TODO

      dBS:              TODO

      dAS:              TODO

      filter_order:     TODO

      dim_time_samples: TODO

      i:                The current index of the data (depends on the current
                        thread / block), has been defined in the global caller.
    */
    T Xii, Yii;

    for (int it = 0; it < dim_time_samples; it++) {
        Xii = input_dx[i * dim_time_samples + it];
        Yii = dBS[0] * Xii + output_dz[i * filter_order];
        tmp_data_dy[i * dim_time_samples + it] = Yii;
        for (int p = 1; p < filter_order; p++) {
            int idx = i * filter_order + p;
            output_dz[idx - 1] = dBS[p] * Xii + output_dz[idx] - dAS[p] * Yii;
        }
    }
}


extern "C" {
    __global__ void filter0_float(const float *input_dx, float *output_dz,
                                  float *tmp_data_dy, const float *vector_b,
                                  const float *vector_a,
                                  const int filter_order,
                                  const int dim_time_samples,
                                  const int nb_data) {
        /* Caller of the "filter0" function on float data, more information in
        its device definition. Also pre-initialize the needed shared memory.
        */
        int i = threadIdx.x + blockIdx.x * blockDim.x;

        // Copy element coordinates into shared memory
        extern __shared__ float shared_mem[];
        float *dBS = &shared_mem[0];
        float *dAS = &shared_mem[filter_order];

        int ti = threadIdx.x;
        if (2 * filter_order <= blockDim.x) {
            if (ti < filter_order) {
                dBS[ti] = vector_b[ti];
            }
            else if (ti < 2 * filter_order) {
                dAS[ti - filter_order] = vector_a[ti - filter_order];
            }
        }
        else {
            while (ti < filter_order) {
                dBS[ti] = vector_b[ti];
                dAS[ti] = vector_a[ti];
                ti += blockDim.x;
            }
        }

        __syncthreads();

        if (i < nb_data) {
            core_filter0(input_dx, output_dz, tmp_data_dy, dBS, dAS,
                         filter_order, dim_time_samples, i);
        }
    }

    __global__ void filter0_complex(const complex<float> *input_dx,
                                    complex<float> *output_dz,
                                    complex<float> *tmp_data_dy,
                                    const float *vector_b,
                                    const float *vector_a,
                                    const int filter_order,
                                    const int dim_time_samples,
                                    const int nb_data) {
        /* Caller of the "filter0" function on complex data, more information
        in its device definition. Also pre-initialize the needed shared memory.
        */
        int i = threadIdx.x + blockIdx.x * blockDim.x;

        // Copy element coordinates into shared memory
        extern __shared__ float shared_mem[];
        float *dBS = &shared_mem[0];
        float *dAS = &shared_mem[filter_order];

        int ti = threadIdx.x;
        if (2 * filter_order <= blockDim.x) {
            if (ti < filter_order) {
                dBS[ti] = vector_b[ti];
            }
            else if (ti < 2 * filter_order) {
                dAS[ti - filter_order] = vector_a[ti - filter_order];
            }
        }
        else {
            while (ti < filter_order) {
                dBS[ti] = vector_b[ti];
                dAS[ti] = vector_a[ti];
                ti += blockDim.x;
            }
        }

        __syncthreads();

        if (i < nb_data) {
            core_filter0(input_dx, output_dz, tmp_data_dy, dBS, dAS,
                         filter_order, dim_time_samples, i);
        }
    }
}
