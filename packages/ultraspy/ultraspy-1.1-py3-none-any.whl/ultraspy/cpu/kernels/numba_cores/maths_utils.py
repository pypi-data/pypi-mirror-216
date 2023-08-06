"""Some utilities for numba.
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def numba_round(x):
    """Returns the rounded value, with upper halves.
        Examples: 0.5 -> 1, 1.5 -> 2, -1.5 -> -2

    :param float x: The value to round

    :returns: Rounded value
    :return type: int
    """
    if x % 1. != 0.5:
        return int(round(x))
    else:
        return int(np.ceil(x) if x > 0 else np.floor(x))
