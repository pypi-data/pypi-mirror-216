"""Methods to compute the distances to a probe using Numba.
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def get_distances(probe, x, y, z, transmission=0):
    """Computes the distances between the pixels to beamform and the probe. It
    also returns the distance in the meridional plane, for aperture evaluation.

    :param numpy.ndarray probe: The probe positions tuple (x_pos, y_pos, z_pos)
    :param float x: The x pixel to compute
    :param float y: The y pixel to compute
    :param float z: The z pixel to compute
    :param int transmission: The transmission index of interest

    :returns: A tuple with: 1) the distances of each element to the position
        (x, y, 0), of the shape (nb_e,) and 2) the distances of the pixel
        (x, y, z) to each element of the probe, of shape (nb_e,)
    :return type: tuple
    """
    lat_p, elev_p, axi_p = probe
    x_diff = x - lat_p[transmission]
    y_diff = y - elev_p[transmission]
    z_diff = z - axi_p[transmission]

    dists = np.sqrt(x_diff ** 2 + y_diff ** 2 + z_diff ** 2)

    return x_diff, y_diff, dists
