"""Constructors for our numpy array masks of different shapes.
"""
import numpy as np


def create_rectangular_mask(top_left, dimension, x_axis, z_axis):
    """Creates a rectangular mask in a numpy array 2D area. The area itself is
    defined by the location of the x and z pixels (in m), and the rectangle
    info are computed with the top-left position and the dimensions of the
    rectangle (expects (width, height)). The top-left and dimensions should
    also be given in m.

    :param tuple top_left: The position of the top-left angle of the rectangle,
        in m
    :param tuple dimension: The dimensions of the rectangle (width, height), in
        m
    :param numpy.ndarray x_axis: The positions of the pixels in X axis, in m
    :param numpy.ndarray z_axis: The positions of the pixels in Z axis, in m

    :returns: The Numpy array of shape (x_axis.size, z_axis.size) with the
        requested mask. The values within the rectangle are not masked, so they
        are set to false, while the rest is set to True (should be masked)
    :return type: numpy.ndarray
    """
    xx, zz = np.meshgrid(x_axis, z_axis)
    return (xx < top_left[0]) | (xx >= top_left[0] + dimension[0]) | \
           (zz < top_left[1]) | (zz >= top_left[1] + dimension[1])


def create_circular_mask(center, radius, x_axis, z_axis):
    """Creates a circular mask in a numpy array 2D area. The area itself is
    defined by the location of the x and z pixels (in m), and the circle
    info are computed with the position of its center and the radius. All are
    expected to be given in m.

    :param tuple center: The center of the circle, in m
    :param float radius: The radius of the circle, in m
    :param numpy.ndarray x_axis: The positions of the pixels in X axis, in m
    :param numpy.ndarray z_axis: The positions of the pixels in Z axis, in m

    :returns: The Numpy array of shape (x_axis.size, z_axis.size) with the
        requested mask. The values within the circle are not masked, so they
        are set to false, while the rest is set to True (should be masked)
    :return type: numpy.ndarray
    """
    xx, zz = np.meshgrid(x_axis, z_axis)
    dist_from_center = np.sqrt((xx - center[0]) ** 2 + (zz - center[1]) ** 2)

    return dist_from_center > radius
