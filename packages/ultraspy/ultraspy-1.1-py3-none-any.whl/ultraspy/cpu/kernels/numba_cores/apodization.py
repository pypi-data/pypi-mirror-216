"""Apodization methods using Numba.
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def boxcar(normed_distance):
    """Boxcar windowing method, checks if the current location is within the
    window, weights 1 if it is, 0 else case.

    :param float normed_distance: The point on which to apply the apodization,
        normed between -1 and 1 (borders of the window)

    :returns: The weight of the boxcar
    :return type: float
    """
    if abs(normed_distance) > 1:
        return 0
    else:
        return 1


@njit(fastmath=True)
def tukey(normed_distance, alpha):
    """Tukey windowing method, apply a tukey factor to a value, supposing it
    has been normalized between -1 and 1. Outside this window, the apodization
    is set to 0, else case, the alpha factor will be applied to get tukey.

    :param float normed_distance: The point on which to apply the apodization,
        normed between -1 and 1 (borders of the window)
    :param float alpha: The Tukey factor to apply

    :returns: The weight of the tukey window (between 0 and 1)
    :return type: float
    """
    dist_to_0 = abs(normed_distance)
    if dist_to_0 > 1:
        return 0
    elif dist_to_0 < 1 - alpha:
        return 1
    else:
        return 0.5 * (1 + np.cos((np.pi / alpha) * (dist_to_0 - 1 + alpha)))


@njit
def get_apodization_weight(normed_distance, factor, method):
    """Factory to return the apodization weights based on the windowing method.

    :param float normed_distance: The point on which to apply the apodization,
        normed between -1 and 1 (borders of the window)
    :param float factor: The Tukey factor to apply
    :param int method: The apodization method, either 0 (boxcar) or 1 (tukey)
    """
    if method == 0:
        return boxcar(normed_distance)
    elif method == 1:
        return tukey(normed_distance, factor)
    else:
        return 0
