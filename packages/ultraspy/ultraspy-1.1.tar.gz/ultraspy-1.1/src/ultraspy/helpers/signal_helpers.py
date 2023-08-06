"""Helpers needed for signal methods.
"""
import numpy as np

from ultraspy.utils import linear_decomposition as utils_linear

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.operators_kernels import (k_flip_old,
                                                        k_flip_within_old)
    from ultraspy.gpu.kernels.signal_kernels import (k_init_filter,
                                                     k_init_start_sig,
                                                     k_filter0,
                                                     k_init_end_sig)


def get_filter_initial_conditions(order, a, b):
    """Returns the initial conditions for filtering. These are used to reduce
    startup and ending transients.
    TODO: read https://www.radioeng.cz/fulltexts/2000/00_02_14_17.pdf
    TODO: maybe remove order? We can extract it with a / b dimensions
    TODO: Maybe p_k would be easier to read in 2d

    :param int order: The order of the filter
    :param numpy.ndarray a: The A coefficients of the filter (see butter)
    :param numpy.ndarray b: The B coefficients of the filter (see butter)

    :returns: The initial conditions for filtering
    :return type: numpy.ndarray
    """
    p_k = np.zeros(order * order)
    for i in range(1, order):
        p_k[i * order + i] = 1
    for i in range(1, order):
        p_k[i * order + 1] = a[i]
        if i == 1:
            p_k[i * order + 1] += 1
    for i in range(1, order - 1):
        p_k[i * order + i + 1] = -1
    new_b = b.copy()
    for i in range(1, order):
        new_b[i] = new_b[i] - a[i] * new_b[0]
    new_b[0] = 0

    # Linear Decomposition
    p_k, idx = utils_linear.ludcmp(p_k, order, np.zeros(order))
    p_b = utils_linear.lubksb(p_k, order, idx, new_b)
    return p_b[1:]


def filtfilt_routine(d_data, nb_data, nb_time_samples, order, d_b, d_a, d_ics,
                     nb_ext, d_x, d_y, d_z):
    """Routine for the filtfilt method, calls the kernels to initialize the
    signals based on the initial conditions and filtering coefficients. The
    filtering is performed on the last dimension, but the d_data array can have
    more than 2 or 3 dimensions. All the operations are performed on GPU, and
    the resulting filtered data is stored in d_data.
    TODO: I think d_y isn't mandatory, it could be replaced by 'd_x2'
    TODO: The dimensions are unclear of tmp arrays to me, it'd worth an
          investigation, especially if it is confusing

    :param cupy.array d_data: The GPUArray data where to apply the filter
        (along the last axis)
    :param np.uint32 nb_data: The number of independent data to filter (all the
        dimensions but the last will be 'flatten' into nb_data samples)
    :param np.uint32 nb_time_samples: The number of time samples along the axis
        to filter (last one)
    :param np.uint32 order: The 'real' order of the filter (note that, in
        butter, we need to give butter(real_order - 1, ...))
    :param cupy.array d_b: The B coefficients of the filter
    :param cupy.array d_a: The A coefficients of the filter
    :param cupy.array d_ics: The initial coefficients of the filter based on
        the above order and a and b coefficients
    :param np.uint32 nb_ext: The number of the bordering values to consider for
        initialisation. It is defined as 3 * (order - 1) in Matlab
        implementation (with order = real_order - 1)
    :param cupy.array d_x: A temporary array of the size (nb_data, nb_ext),
        used to store the initial or ending values of the signals
    :param cupy.array d_y: A temporary array of the size (nb_data,
        nb_time_samples), used to store the filtered results without affecting
        the initial data
    :param cupy.array d_z: A temporary array of the size (real_order, nb_data),
        used to store the filtering coefficients as they are updated
    """
    # Block / Grid sizes depending on operation
    g_dim_1, b_dim_1 = gpu_utils.compute_flat_grid_size(int(nb_data))
    g_dim_2, b_dim_2 = gpu_utils.compute_flat_grid_size(d_z.size)
    g_dim_3, b_dim_3 = gpu_utils.compute_flat_grid_size(d_data.size)

    # Initialize beginning of the signal and filters it using the initial
    # conditions we've defined previously
    k_init_start_sig(g_dim_1, b_dim_1,
                     (d_data, d_x, nb_ext, nb_time_samples, nb_data))
    k_init_filter(g_dim_2, b_dim_2,
                  (d_x, d_z, d_ics, order, nb_ext, nb_data))
    k_filter0(g_dim_1, b_dim_1,
              (d_x, d_z, d_x, d_b, d_a, order, nb_ext, nb_data),
              shared_mem=int(order))

    # Forward filtering of the data
    k_filter0(g_dim_1, b_dim_1,
              (d_data, d_z, d_y, d_b, d_a, order, nb_time_samples, nb_data),
              shared_mem=int(order))

    # Initialize the end of the signal and filters it using the initial
    # conditions we've defined previously, then flips it so it matches the
    # reversed orientation
    k_init_end_sig(g_dim_1, b_dim_1,
                   (d_data, d_x, nb_ext, nb_time_samples, nb_data),
                   shared_mem=int(order))
    k_filter0(g_dim_1, b_dim_1,
              (d_x, d_z, d_x, d_b, d_a, order, nb_ext, nb_data),
              shared_mem=int(order))
    k_flip_old(g_dim_3, b_dim_3, (d_x, nb_ext, nb_data))

    # Initialize the beginning of the reversed signal and filters it the same
    # way as the first one, using ICs, then flips it
    k_init_filter(g_dim_2, b_dim_2,
                  (d_x, d_z, d_ics, order, nb_ext, nb_data))
    k_filter0(g_dim_1, b_dim_1,
              (d_x, d_z, d_x, d_b, d_a, order, nb_ext, nb_data),
              shared_mem=int(order))

    # Backward filtering of the data
    k_flip_old(g_dim_3, b_dim_3, (d_y, nb_time_samples, nb_data))
    k_filter0(g_dim_1, b_dim_1,
              (d_y, d_z, d_y, d_b, d_a, order, nb_time_samples, nb_data),
              shared_mem=int(order))

    # Flip result to get original orientation
    k_flip_within_old(g_dim_3, b_dim_3,
                      (d_y, d_data, nb_time_samples, nb_data))
