"""Methods for interpolation with numpy.
"""
import numpy as np
from scipy.interpolate import interp1d


def no_interpolation(data, indices):
    """No interpolation, just convert into the nearest index.

    :param numpy.ndarray data: The RFs or I/Qs to beamform, of shape (nb_t,
        nb_re, nb_ts)
    :param numpy.ma.masked_array indices: The indices for the time samples
        vector. The data we are looking for is theoretically
        data[ie, grid[ie, :]]. It is expected to be of the shape (nb_t, nb_re,
        nb_p)

    :returns: The interpolated data, of the same shape as indices
    :return type: numpy.ma.masked_array
    """
    nb_t, nb_re, nb_ts = data.shape
    out = ((indices < 0) & (indices > nb_ts - 1))
    indices = np.round(indices).clip(0, nb_ts - 1).astype(int)

    idx_t = np.arange(nb_t)[:, None, None].astype(int)
    idx_re = np.arange(nb_re)[None, :, None].astype(int)
    idx = idx_t, idx_re, indices
    interpolated = np.ma.masked_array(data[idx], indices.mask)

    interpolated[out] = 0
    return interpolated


def linear_interpolation(data, indices):
    """Linear interpolation, finds the two bound values, and return an
    in-between interpolation.

    :param numpy.ndarray data: The RFs or I/Qs to beamform, of shape (nb_t,
        nb_re, nb_ts)
    :param numpy.ma.masked_array indices: The indices for the time samples
        vector. The data we are looking for is theoretically
        data[ie, grid[ie, :]]. It is expected to be of the shape (nb_t, nb_re,
        nb_p)

    :returns: The interpolated data, of the same shape as indices
    :return type: numpy.ma.masked_array
    """
    nb_t, nb_re, nb_ts = data.shape
    out = ((indices < 0) & (indices > nb_ts - 1))

    indices = indices.clip(0, nb_ts - 1)
    lower = np.floor(indices).astype(int)
    upper = np.ceil(indices).astype(int)

    # Calculate the weights for the linear interpolation
    frac = indices - lower
    w1 = 1 - frac
    w2 = frac

    # Transmissions / elements indices
    idx_t = np.arange(nb_t)[:, None, None].astype(int)
    idx_re = np.arange(nb_re)[None, :, None].astype(int)

    # Get the lower / upper values
    interp_lower = data[idx_t, idx_re, lower]
    interp_upper = data[idx_t, idx_re, upper]

    # Interpolation
    interpolated = np.ma.masked_array(interp_lower * w1 + interp_upper * w2,
                                      indices.mask)

    interpolated[out] = 0
    return interpolated


def quadratic_interpolation(data, indices):
    """Quadratic interpolation.
    TOOD

    :param numpy.ndarray data: The RFs or I/Qs to beamform, of shape (nb_t,
        nb_re, nb_ts)
    :param numpy.ndarray indices: The indices for the time samples vector. The
        data we are looking for is theoretically data[ie, grid[ie, :]]. It is
        expected to be of the shape (nb_t, nb_re, nb_p)

    :returns: The interpolated data, of the same shape as indices
    :return type: numpy.ndarray
    """
    nb_e, nb_ts = data.shape
    container = np.zeros_like(indices).astype(data.dtype)
    for ie in range(nb_e):
        interp = interp1d(np.arange(nb_ts), data[ie],
                          kind='quadratic', bounds_error=False, fill_value=0)
        container[ie, :] = interp(indices[ie])
    return container


def cubic_interpolation(data, indices):
    """Cubic interpolation.
    TOOD

    :param numpy.ndarray data: The RFs or I/Qs to beamform, of shape (nb_t,
        nb_re, nb_ts)
    :param numpy.ndarray indices: The indices for the time samples vector. The
        data we are looking for is theoretically data[ie, grid[ie, :]]. It is
        expected to be of the shape (nb_t, nb_re, nb_p)

    :returns: The interpolated data, of the same shape as indices
    :return type: numpy.ndarray
    """
    nb_e, nb_ts = data.shape
    container = np.zeros_like(indices).astype(data.dtype)
    for ie in range(nb_e):
        interp = interp1d(np.arange(nb_ts), data[ie],
                          kind='cubic', bounds_error=False, fill_value=0)
        container[ie, :] = interp(indices[ie])
    return container


def interpolate(data, indices, method):
    """The factory for the interpolation method. It is expected 'method' to be
    either 'none', 'linear', 'quadratic' or 'cubic'.

    :param numpy.ndarray data: The RFs or I/Qs to beamform, of shape (nb_t,
        nb_re, nb_ts)
    :param numpy.ma.masked_array indices: The indices for the time samples
        vector. The data we are looking for is theoretically
        data[ie, grid[ie, :]]. It is expected to be of the shape (nb_t, nb_re,
        nb_p)
    :param int method: The name of the interpolation method to use

    :returns: The interpolated data, of the same shape as indices
    :return type: numpy.ma.masked_array
    """
    return {
        0: no_interpolation,
        1: linear_interpolation,
        2: quadratic_interpolation,
        3: cubic_interpolation,
    }[method](data, indices)
