"""Methods for data filtering. These aim to be accessible by users.
"""
import numpy as np
import scipy.signal

from ultraspy.helpers.signal_helpers import (get_filter_initial_conditions,
                                             filtfilt_routine)

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.operators_kernels import (k_by2,
                                                        k_divide_by,
                                                        k_max,
                                                        k_convolve1d)
    from ultraspy.gpu.kernels.signal_kernels import k_down_mix


def down_mix(d_data, central_freq, sampling_freq, t0, axis=-1, inplace=True):
    """Down-mixing operation, performs a phase rotation on our data to move the
    spectrum around 0 Hz (involving the returned signal to be complex). The
    down-mixing is performed along the time axis (last one by default). All the
    operations are performed on GPU using a CUDA kernel.

    :param cupy.array d_data: The GPUArray data on which to perform the
        down-mixing (along last dimension). It must be of a complex type as the
        down-mixing will return a complex array
    :param float central_freq: The central frequency of the signal (in Hz)
    :param float sampling_freq: The sampling frequency of the signal (in Hz)
    :param float t0: The t0 of the recorded samples (in s)
    :param int axis: The axis of the data to filter
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept.

    :returns: The down-mixed data if inplace is False, else case return None
        and d_data is modified directly
    :return type: None, cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        down_mix(d_new, central_freq, sampling_freq, t0)
        return d_new

    if d_data.dtype != np.dtype('complex64'):
        d_data = d_data.astype(np.complex64)

    if axis != -1 and axis != d_data.ndim - 1:
        d_data = gpu_utils.swap_axes(d_data, axis, -1)

    nb_x = int(np.prod(d_data.shape[:-1]))
    nb_z = d_data.shape[-1]
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_down_mix(g_dim, b_dim,
               (d_data, np.int32(nb_z), np.int32(nb_x), np.float32(t0),
                np.float32(central_freq), np.float32(sampling_freq)))

    if axis != -1 and axis != d_data.ndim - 1:
        gpu_utils.set_values(d_data, gpu_utils.swap_axes(d_data, -1, axis))


def filtfilt(d_data, bound, sampling_freq, filter_type, order=5, axis=-1,
             inplace=True):
    """Butterworth filtfilt, greatly inspired by Matlab's filtfilt version,
    zero-phase forward and reverse digital filtering using CUDA kernels, it
    filters data using coefficients A and B describing the following difference
    equation:

    | y(n) = b(1)*x(n) + b(2)*x(n-1) + ... + b(nb+1)*x(n-nb)
    |                  - a(2)*y(n-1) - ... - a(na+1)*y(n-na)

    with `b` and `a`, the coefficients we computed from the butter function
    (scipy).

    :param cupy.array d_data: The GPUArray data where to apply the filter
        (along the last axis)
    :param float bound: The critical frequency for the filtering, in Hz
    :param float sampling_freq: The sampling frequency of the signal, in Hz
    :param str filter_type: The type of the filter ('low' or 'high')
    :param int order: The order of the filter (default to 5)
    :param int axis: The axis of the data to filter
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The filtered data if inplace is False, else case return None and
        d_data is modified directly
    :return type: None, cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        filtfilt(d_new, bound, sampling_freq, filter_type, order, axis)
        return d_new

    supported = ['low', 'high']
    if filter_type not in supported:
        raise AttributeError(
            f"Unknown filter type '{filter_type}', pick one among {supported}.")

    if axis != -1 and axis != d_data.ndim - 1:
        d_tmp = gpu_utils.swap_axes(d_data, axis, -1)
    else:
        d_tmp = d_data

    nyquist_frequency = sampling_freq / 2
    w_n = bound / nyquist_frequency

    if w_n <= 0 or w_n >= 1:
        raise ValueError(
            f"The critical frequency ({bound}) should be between 0 and "
            f"{nyquist_frequency}Hz.")

    _filtfilt_wn(d_tmp, w_n, filter_type, order)

    if axis != -1 and axis != d_data.ndim - 1:
        gpu_utils.set_values(d_data, gpu_utils.swap_axes(d_tmp, -1, axis))
    else:
        gpu_utils.set_values(d_data, d_tmp)


def rf2iq(d_data, central_freq, sampling_freq, t0, order=5, bandwidth=100,
          axis=-1, implementation='all_in_one', inplace=True):
    """Converts raw RFs data signals into I/Qs (In-Phase Quadrature) using
    CUDA kernels on GPU. Consists in a down-mixing operation (centers the
    spectrum at 0Hz), followed by a low-pass filter to keep only the newly
    centered at 0 spectrum (remove the old negative component). Note that it
    assumes that the time samples (fast time) are in the last axis of d_data.

    TODO: Not exactly the same for envelope from RFs, should check

    :param cupy.array d_data: The GPUArray data to convert (along the last axis)
    :param float central_freq: The central frequency of the signal
    :param float sampling_freq: The sampling frequency of the data
    :param float t0: The initial time of recording (in s)
    :param int order: The order of the low-pass filter
    :param int axis: The axis of the data to convert
    :param float bandwidth: The bandwidth of the probes. Default is set to 100,
        which means that the whole information is supposed (1. x f0)-wide,
        centered at f0. Thus, the low-pass filter is set to half
        (bandwidth x f0)
    :param str implementation: The implementation to use for filtfilt (can be
        'memory_handler', 'all_in_one' or 'unique_coefficients')
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The converted data (I/Qs) if inplace is False, else case return
        None and d_data is modified directly
    :return type: None, cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        rf2iq(d_new, central_freq, sampling_freq, t0, order, bandwidth, axis,
              implementation)
        return d_new

    if axis != -1 and axis != d_data.ndim - 1:
        d_data = gpu_utils.swap_axes(d_data, axis, -1)

    # Demodulation
    down_mix(d_data, central_freq, sampling_freq, t0, axis=-1)

    # Low pass filter, half Fc in both positive / negative frequencies
    bandwidth /= 100
    half_central = central_freq * (bandwidth / 2)
    half_central = min(half_central, sampling_freq / 4)
    filtfilt(d_data, half_central, sampling_freq, 'low', order, axis=-1)

    # We removed half the frequencies during filtering, need to preserve the
    # amplitudes
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_by2(g_dim, b_dim, (d_data, np.uint32(d_data.size)))

    if axis != -1 and axis != d_data.ndim - 1:
        gpu_utils.set_values(d_data, gpu_utils.swap_axes(d_data, -1, axis))


def matched_filter(d_data, ref_signal, domain='time', inplace=True):
    """Applies a matched filter to our data along the last axis, given a
    reference signal which is supposed to match. Only the version on time
    domain currently works, which is basically a cross-correlation of our data
    with the reference signal, using a zero padding to keep it center all the
    time.

    TODO: Didn't work on chirps tests (consecutive calls), check TODO list

    :param cupy.array d_data: The GPUArray data where to apply the filter
        (along the last axis)
    :param numpy.ndarray ref_signal: The reference signal (1D)
    :param str domain: The domain to use ('time' (default) or 'spectral')
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The match filtered data if inplace is False, else case return
        None and d_data is modified directly
    :return type: None, cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        matched_filter(d_new, ref_signal, domain)
        return d_new

    if domain not in ['time']:
        raise NotImplementedError("Unknown domain to work on. Only 'time' is "
                                  "currently supported.")

    # Data and filter information
    nb_data = int(np.prod(d_data.shape[:-1]))
    nb_time_samples = d_data.shape[-1]
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)

    # Send to GPU
    d_tmp = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
    d_kernel = gpu_utils.send_to_gpu(np.array(ref_signal), np.float32)
    k_convolve1d(g_dim, b_dim,
                 (d_data, d_tmp, d_kernel, np.uint32(nb_data),
                  np.uint32(nb_time_samples), np.uint32(ref_signal.size)))
    gpu_utils.set_values(d_data, d_tmp)


def normalize(d_data, ref_value=None, inplace=True):
    """Simply normalizes a signal to values between -1 and 1. Note that it only
    works on float signals (RFs).

    :param cupy.array d_data: The GPUArray data to normalize
    :param float ref_value: A reference value for normalization, if set, the
        normalization will be done using the reference value.
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The match filtered data if inplace is False, else case return
        None and d_data is modified directly
    :return type: None, cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        normalize(d_new, ref_value)
        return d_new

    # Normalize
    if ref_value is None:
        ref_value = k_max(abs(d_data))

    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_divide_by(g_dim, b_dim,
                (d_data, np.float32(ref_value), np.uint32(d_data.size)))


def _filtfilt_wn(d_data, w_n, filter_type, order=5):
    """Calls the filtfilt routine in an independent way: it creates itself the
    temporary needed arrays and those are destroyed after each use.

    :param cupy.array d_data: The GPUArray data where to apply the filter
        (along the last axis)
    :param float w_n: The critical frequency (normalized between 0 and 1, with
        1 the nyquist frequency)
    :param str filter_type: The type of the filter ('low' or 'high')
    :param int order: The order of the filter (default to 5)
    """
    # Filtering coefficients
    b, a = scipy.signal.butter(order, w_n, btype=filter_type)

    # Data and filter information
    nb_data = int(np.prod(d_data.shape[:-1]))
    nb_time_samples = d_data.shape[-1]
    ics = get_filter_initial_conditions(order + 1, a, b)
    nb_ext = 3 * (order - 1)

    # Send to GPU
    d_b = gpu_utils.send_to_gpu(b, np.float32)
    d_a = gpu_utils.send_to_gpu(a, np.float32)
    d_ics = gpu_utils.send_to_gpu(ics, np.float32)
    d_x = gpu_utils.initialize_empty((nb_data, nb_ext), np.complex64)
    d_y = gpu_utils.initialize_empty((nb_time_samples, nb_data), np.complex64)
    d_z = gpu_utils.initialize_empty((order + 1, nb_data), np.complex64)
    real_order = np.uint32(order + 1)
    nb_ext = np.uint32(nb_ext)
    nb_data = np.uint32(nb_data)
    nb_time_samples = np.uint32(nb_time_samples)

    filtfilt_routine(d_data, nb_data, nb_time_samples, real_order, d_b, d_a,
                     d_ics, nb_ext, d_x, d_y, d_z)
