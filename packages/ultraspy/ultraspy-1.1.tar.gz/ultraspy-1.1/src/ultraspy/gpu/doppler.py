"""Methods for doppler imaging.
"""
import logging
import numpy as np

from ultraspy.helpers.doppler_helpers import get_polynomial_coefficients
from ultraspy.helpers.windows_helpers import get_hamming_squared_kernel
import ultraspy as us

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    import cupyx.scipy.ndimage

    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.operators_kernels import (k_divide_by,
                                                        k_power_to_db,
                                                        k_max,
                                                        k_convolve2d)
    from ultraspy.gpu.kernels.doppler_kernels import (k_mean_wall_filter,
                                                      k_poly_wall_filter,
                                                      k_correlation_matrix,
                                                      k_color_map,
                                                      k_power_map)


logger = logging.getLogger(__name__)


def apply_wall_filter(d_data, mode, degree=1, inplace=True):
    """Applies a clutter filter along slow time (last dimension of our data by
    default). Four modes are available:

        - none: when there are no wall filter to apply, doesn't do anything
        - mean: applies a basic mean filter (subtract the mean of the data
          along slow time)
        - poly: applies a polynomial filter. The polynomial regression consists
          in using orthogonal Legendre polynomial coefficients to remove the
          fitting polynomials from the data, which ends up to remove the low
          frequencies components. The degree is the upper degree of the
          polynomials we want to remove
        - hp_filter: applies a high-pass butterworth filter. The critical
          frequency is assumed to be a tenth of degree (HP filter of everything
          above 10% of the spectrum if degree = 1)

    :param cupy.array d_data: The GPUArray on which to perform the clutter
        filter
    :param str mode: The name of the clutter filter to use, can be 'none',
        'mean', 'poly' or 'hp_filter'
    :param int degree: The order of our filter (or 10 * w_n if we do hp_filter)
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The filtered data along slow time if inplace is False, else case
        return None and d_data is modified directly
    :return type: cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        apply_wall_filter(d_new, mode, degree)
        return d_new

    # No wall filter, do nothing
    if mode == 'none':
        return

    # Mean wall filter
    if mode == 'mean' or degree == 0:
        _apply_mean_wall_filter(d_data)

    # Polynomial wall filter
    elif mode == 'poly':
        _apply_poly_wall_filter(d_data, degree)

    # High-pass wall filter
    elif mode == 'hp_filter':
        w_n = degree / 10
        _apply_hp_wall_filter(d_data, w_n)

    # Unknown clutter filter
    else:
        raise AttributeError(
            f"Unknown wall filter. Please choose one of  the following: "
            f"none, mean, poly, hp_filter")


def spatial_smoothing(d_data, k_size, window_type='hamming', inplace=True):
    """Performs a spatial smoothing on data, using a given window function to
    compute the squared convolution kernel... Two methods are implemented:

        - hamming: Performs a convolution with a squared hamming window of size
          (k_size, k_size)
        - median: applies a median filter on a squared spatial matrix (of size
          (k_size, k_size)). If complex numbers, do the median of both real and
          imaginary parts separately

    TODO: Median smoother is very slow for big sizes (expected by cupyx, as
        detailed in github.com/cupy/cupy/issues/6453)

    :param cupy.array d_data: The 2D GPUArray data stored on GPU, of dtype
        complex64 or float32
    :param int k_size: The kernel size. Works better if it is an odd number, as
        the kernel can be centered on each pixel.
    :param str window_type: The name of the windowing function to use, only
        'hamming' (default) and 'median' are supported for now.
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The smoothed data if inplace is False, else case return None and
        d_data is modified directly
    :return type: cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        spatial_smoothing(d_data, k_size, window_type)
        return d_new

    if window_type not in ['hamming', 'median']:
        raise AttributeError(
            f"Unknown window type function, please peak among supported "
            f"methods (hamming or median).")

    if k_size % 2 == 0:
        k_size += 1
        logger.warning("Smoothing doesn't work properly on GPU with even "
                       f"dimensions, changed k_size to {k_size}.")

    if k_size > 1:
        if window_type == 'median':
            # Use cupyx
            if d_data.imag.any():
                d_data.real = cupyx.scipy.ndimage.median_filter(
                    d_data.real, k_size, mode='nearest')
                d_data.imag = cupyx.scipy.ndimage.median_filter(
                    d_data.imag, k_size, mode='nearest')
            else:
                gpu_utils.set_values(d_data, cupyx.scipy.ndimage.median_filter(
                    d_data, k_size, mode='nearest'))

            # nb_x, nb_y = d_data.shape
            # d_tmp = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
            # g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_x * nb_y)
            # k_median_filter(g_dim, b_dim,
            #                 (d_data, d_tmp, np.uint32(nb_x), np.uint32(nb_y),
            #                  np.uint32(k_size)))
            # gpu_utils.set_values(d_data, d_tmp)
        else:
            nb_x, nb_y = d_data.shape
            k = get_hamming_squared_kernel(k_size)
            d_tmp = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
            d_kernel = gpu_utils.send_to_gpu(k, np.float32)
            g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
            k_convolve2d(g_dim, b_dim,
                         (d_data, d_tmp, d_kernel, np.uint32(nb_x),
                          np.uint32(nb_y), np.uint32(k_size)))
            gpu_utils.set_values(d_data, d_tmp)


def get_color_doppler_map(d_data, nyquist_velocity, smoothing='hamming',
                          kernel=1):
    """Computes the color doppler map, which is using the correlation of our
    data along slow time (last dimension of data), which are then converted to
    doppler velocity using the Doppler formula. It also can perform a spatial
    smoothing of a given number of pixels.

    .. math::
        v_{D} = -v_{c} . \\Im \\left (\\frac{\\log(data)}{\\pi} \
                              \\right )

    :param cupy.array d_data: The GPUArray data stored on GPU, of dtype
        complex64
    :param float nyquist_velocity: The nyquist velocity, can be determined
        using c * prf / (4 * f_c)
    :param str smoothing: The smoothing method to use (either hamming or median)
    :param int kernel: The size of the squared kernel for smoothing

    :returns: The color map, which is of the shape of d_data (except the slow
        time dimension), and of type np.float32
    :return type: cupy.array
    """
    # Could be inplace, but good choice?
    nb_pixels = int(np.prod(d_data.shape[:-1]))
    nb_frames = d_data.shape[-1]
    d_color_doppler = gpu_utils.initialize_empty(d_data.shape[:-1],
                                                 np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
    k_correlation_matrix(g_dim, b_dim,
                         (d_data, d_color_doppler, np.uint32(nb_frames),
                          np.uint32(nb_pixels)))
    spatial_smoothing(d_color_doppler, kernel, smoothing)
    k_color_map(g_dim, b_dim,
                (d_color_doppler, np.float32(nyquist_velocity),
                 np.uint32(nb_pixels)))
    return d_color_doppler.real.astype(np.float32)


def get_power_doppler_map(d_data, smoothing='hamming', kernel=1):
    """Computes the power doppler map, which is using the mean of squared
    values along slow time (defined as the last dimension of data). The result
    is then returned in dB. It can also perform a spatial smoothing of a given
    number of pixels.

    .. math::
        \\text{MS} = \\frac{\\sum_{i=1}^{n}{|\\text{data}_{\\ i}|^2}}{n}

        P_{D} = 10 . \\frac{\\log_{10}(\\text{MS})}{\\max(\\text{MS})}

    :param cupy.array d_data: The GPUArray data stored on GPU, of dtype
        complex64
    :param str smoothing: The smoothing method to use (either hamming or median)
    :param int kernel: The size of the squared kernel for smoothing

    :returns: The power map, which is of the shape of d_data (except the slow
        time dimension), and of type np.float32
    :return type: cupy.array
    """
    # Could be inplace, but good choice?
    nb_pixels = int(np.prod(d_data.shape[:-1]))
    nb_frames = d_data.shape[-1]
    d_power_doppler = gpu_utils.initialize_empty(d_data.shape[:-1], np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
    k_power_map(g_dim, b_dim,
                (d_data, d_power_doppler, np.uint32(nb_frames),
                 np.uint32(nb_pixels)))
    spatial_smoothing(d_power_doppler, kernel, smoothing)
    k_divide_by(g_dim, b_dim,
                (d_power_doppler, np.float32(k_max(d_power_doppler)),
                 np.uint32(nb_pixels)))
    k_power_to_db(g_dim, b_dim, (d_power_doppler, np.uint32(nb_pixels)))
    return d_power_doppler


def _apply_mean_wall_filter(d_data):
    """Applies a basic mean filter on our data along slow time (last axis). It
    simply subtracts the mean of the pixels along slow time.

    :param cupy.array d_data: The GPUArray data stored on GPU, of dtype
        complex64
    """
    nb_pixels = int(np.prod(d_data.shape[:-1]))
    dim_slow_time = d_data.shape[-1]

    # Performs the filter on GPU
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
    k_mean_wall_filter(g_dim, b_dim,
                       (d_data, np.uint32(dim_slow_time),
                        np.uint32(nb_pixels)))


def _apply_poly_wall_filter(d_data, degree):
    """Applies a polynomial clutter filter on our data along slow time (should
    be the last axis). The polynomial regression consists in using orthogonal
    Legendre polynomial coefficients to remove the fitting polynomials from the
    data, which ends up to remove the low frequencies components. The degree is
    the upper degree of the polynomials we want to remove.

    TODO: Test with the MemoryHandler

    :param cupy.array d_data: The GPUArray data stored on GPU, of dtype
        complex64
    :param int degree: The upper degree of the polynomials we want to remove
    """
    nb_pixels = int(np.prod(d_data.shape[:-1]))
    nb_frames = d_data.shape[-1]
    polys = get_polynomial_coefficients(nb_frames, degree)

    # Performs the filter on GPU
    d_polys = gpu_utils.send_to_gpu(polys, np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
    k_poly_wall_filter(g_dim, b_dim,
                       (d_data, d_polys, np.uint32(degree),
                        np.uint32(nb_frames), np.uint32(nb_pixels)))


def _apply_hp_wall_filter(d_data, w_n):
    """Applies a high-pass butterworth filter on our data along slow time which
    should be the last dimension. The w_n parameter is the critical frequency
    where the gain will drop to 1 / sqrt(2). As we are working with digital
    filters, it is normalized from 0 to 1 where 1 is the Nyquist frequency. The
    clutter filter is performed on GPU, and will modify d_data directly.

    TODO: There is still a choice that need to be done here: should we peak
          pycuda_filtfilt2..? 3..? or 1?

    :param cupy.array d_data: The GPUArray data stored on GPU, of dtype
        complex64
    :param float w_n: The normalized critical frequency to use for filtering
    """
    us.gpu.signal._filtfilt_wn(d_data, w_n, 'high')
