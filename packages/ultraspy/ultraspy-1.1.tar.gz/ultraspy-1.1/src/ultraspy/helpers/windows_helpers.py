"""Helpers needed for windowing functions. These run on CPU but are considered
fast enough, and those shouldn't be accessible by users.
"""
import numpy as np


def get_hamming_squared_kernel(k_size):
    """Returns a squared matrix filled with hamming vectors multiplied by
    themselves.

    :param int k_size: The size of the kernel border

    :returns: The hamming kernel of shape (k_size, k_size)
    :return type: numpy.ndarray
    """
    vector = np.hamming(k_size)
    return vector[:, None] * vector
