"""Helpers for beamformers.
Formula in: en.wikipedia.org/wiki/Spherical_coordinate_system
TODO
"""
import numpy as np


def pol2cart(rhos, phis):
    """TODO
    """
    x = rhos * np.sin(phis)
    z = rhos * np.cos(phis)
    return x, z


def pol2cart_3d(rhos, phis, thetas):
    """TODO (stackoverflow.com/questions/20769011)
    """
    x = rhos * np.sin(phis) * np.cos(thetas)
    y = rhos * np.cos(phis) * np.sin(thetas)
    z = rhos * np.cos(phis)
    return x, y, z
