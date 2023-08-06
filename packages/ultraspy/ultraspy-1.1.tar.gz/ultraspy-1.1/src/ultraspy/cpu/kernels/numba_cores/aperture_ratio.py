"""Methods to compute the apertures ratio based on probe geometry using Numba.
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def get_aperture_ratio(z, x_diff, y_diff, dist, theta, f_number):
    """Returns the ratio telling if the element is within the aperture of the
    probe element. This is normalized, everything between [-1, 1] is within
    aperture, outside else case.

    :param numpy.ndarray z: The axial coordinates of the pixels
    :param numpy.ndarray x_diff: The difference between the lateral probe
        elements and the lateral coordinates of the pixels, of shape
        (nb_transmissions, nb_elements, nb_pixels)
    :param numpy.ndarray y_diff: The difference between the elevational probe
        elements and the elevational coordinates of the pixels, of shape
        (nb_transmissions, nb_elements, nb_pixels)
    :param numpy.ndarray dist: The distance between the lateral probe
        elements and all the pixels, of shape (nb_transmissions, nb_elements,
        nb_pixels)
    :param numpy.ndarray theta: The theta of the probe element
        (nb_transmissions, nb_elements)
    :param numpy.ndarray f_number: The f number, full aperture if =0.
        Two-dimensional, for both the lateral and elevational axes

    :returns: The ratio of the aperture, within if [-1, 1], outside else case
    :return type: numpy.ndarray
    """
    # If f-number is 0, full aperture is used, so we set the ratios to 0
    # (each pixel is considered in sight of each element of the probe)
    if (f_number == 0).any():
        return np.zeros_like(dist)

    # If there is a theta for this element, we compute the aperture using the
    # difference between the thetas, only works in convex probes (2D)
    elif theta.any():
        aperture = np.arctan(1 / (2 * f_number[0]))
        return (np.arcsin(x_diff / dist) - theta) / aperture

    # Else case, flat probe, we're using the depth
    else:
        aperture1 = np.abs(x_diff) / (z / (2 * f_number[0]))
        aperture2 = np.abs(y_diff) / (z / (2 * f_number[1]))
        for i in range(aperture1.size):
            aperture1[i] = max(aperture1[i], aperture2[i])
        return aperture1


@njit(fastmath=True)
def set_to_inf(distances, ratios):
    """Returns the distances with infinite value for the elements where the
    ratio is outside [-1, 1] (not within the probe aperture).

    :param numpy.ndarray distances: The distances to the probe (nb_e,)
    :param numpy.ndarray ratios: The ratios for each element (nb_e,)

    :returns: The distances with infinite where out of bound
    :return type: float
    """
    for i in range(ratios.size):
        if abs(ratios[i]) > 1:
            distances[i] = np.Inf
    return distances
