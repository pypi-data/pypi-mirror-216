"""Methods to compute the distances to a probe.
"""
import numpy as np


def get_distances(probe, xs, ys, zs):
    """Computes the distances between the pixels to beamform and the probe. It
    also returns the distance in the meridional plane, for aperture evaluation.

    :param numpy.ndarray probe: The probe positions tuple (x_pos, y_pos, z_pos)
    :param numpy.ndarray xs: The lateral pixels coordinates of the scan
    :param numpy.ndarray ys: The elevational pixels coordinates of the scan
    :param numpy.ndarray zs: The axial pixels coordinates of the scan

    :returns: A tuple with: 1) the distances of each element to each lateral
        position of the scan, of the shape (nb_e, nb_p / nb_z) and 2) the
        distances of each pixel of the scan to the probe, of shape (nb_e, nb_p)
    :return type: tuple
    """
    lat_p, elev_p, axi_p = probe

    x_diff = xs - lat_p[..., None]
    y_diff = ys - elev_p[..., None]
    z_diff = zs - axi_p[..., None]

    dists = np.sqrt(x_diff ** 2 + y_diff ** 2 + z_diff ** 2)

    return x_diff, y_diff, dists
