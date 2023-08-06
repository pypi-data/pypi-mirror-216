"""Interpolation methods using Numba.
"""
from numba import njit

from .maths_utils import numba_round


@njit(fastmath=True)
def no_interpolation(real_index, signal):
    """No interpolation, just convert into the nearest index.

    :param float real_index: The index we've computed, that need to be rounded
    :param numpy.ndarray signal: The RFs or I/Qs data

    :returns: The closest data sample
    :return type: signal.dtype
    """
    idx = numba_round(real_index)
    if 0 <= idx < len(signal):
        return signal[idx]
    return None


@njit(fastmath=True)
def linear(real_index, signal):
    """Linear interpolation, finds the two bound values, and return an
    in-between interpolation.

    :param float real_index: The index we've computed, that need to be
        interpolated
    :param numpy.ndarray signal: The RFs or I/Qs data

    :returns: The interpolated data
    :return type: signal.dtype
    """
    idx = int(real_index)
    if 0 <= idx < len(signal) - 1:
        dl = signal[idx]
        du = signal[idx + 1]
        t = real_index - idx
        return dl * (1 - t) + du * t
    return None


@njit
def interpolate(real_index, signal, method):
    """The factory for the interpolation method. It is expected 'method' to be
    either 'none' or 'linear'.

    :param float real_index: The index we've computed, that need to be
        interpolated
    :param numpy.ndarray signal: The RFs or I/Qs data
    :param int method: The name of the interpolation method to use

    :returns: The interpolated data
    :return type: signal.dtype
    """
    if method == 0:
        return no_interpolation(real_index, signal)
    elif method == 1:
        return linear(real_index, signal)
    else:
        return None
