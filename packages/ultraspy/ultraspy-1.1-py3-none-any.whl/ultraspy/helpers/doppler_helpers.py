"""Helpers needed for Doppler. Those run on CPU but are considered fast enough
to be used in parallel with GPU methods.
"""
import numpy as np


def get_polynomial_coefficients(dim_slow_time, degree, normalize=False):
    """Returns the orthogonal Legendre polynomial coefficients to operate the
    least squares (at nth degree) polynomial regression. It will then be used
    for clutter filter.

    :param int dim_slow_time: The number of frames we are considering along the
        slow time
    :param int degree: The degree for the polynomial regression
    :param bool normalize: If set to True, the returned polynomials are ranged
        within -1 and 1

    :returns: The orthogonal polynomial coefficients, of size
        ((degree + 1), dim_slow_time)
    :return type: numpy.ndarray
    """
    # We first create the orthogonal polynomial (Legendre) family: PL contains
    # the orthogonal polynomials i.e.
    # PL(k, :) = polynomial or order (k-1)
    polys = np.ones((degree + 1, dim_slow_time))
    x_ls = np.linspace(-1, 1, dim_slow_time)

    polys[1, :] = x_ls  # - np.mean(x_ls)  # mean is 0
    for i in range(2, degree + 1):
        pm1, pm2 = polys[i - 1, :], polys[i - 2, :]
        tmp1 = np.sum(x_ls * (pm1 ** 2)) / np.sum(pm1 ** 2)
        tmp2 = np.sum(x_ls * pm2 * pm1) / np.sum(pm2 ** 2)
        polys[i, :] = (x_ls - tmp1) * pm1 - tmp2 * pm2

    # To make them fit the range (-1, 1)
    if normalize:
        polys /= polys[:, -1:]

    return polys
