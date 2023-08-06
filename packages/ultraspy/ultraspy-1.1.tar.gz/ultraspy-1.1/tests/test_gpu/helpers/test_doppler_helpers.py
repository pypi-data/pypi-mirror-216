"""Unit test file for all the helpers used in Doppler.
"""
import numpy as np

from ultraspy.helpers.doppler_helpers import get_polynomial_coefficients


def test_get_polynomial_coefficients():
    # We test the orthogonal coefficients for the first few degrees
    nb_data = 100
    p2 = get_polynomial_coefficients(nb_data, 2)
    p5 = get_polynomial_coefficients(nb_data, 5)
    p10 = get_polynomial_coefficients(nb_data, 10)
    assert np.all(p10[1] == p5[1])
    assert np.all(p10[1] == p2[1])
    assert np.all(p10[4] == p5[4])

    # We should compare the approximation we compute vs the real coefficients
    # we've found on wikipedia (en.wikipedia.org/wiki/Legendre_polynomials).
    # We consider our approximation should have an error below (nb_data / 10)%
    # of the point to point value (min to max).
    p10 = get_polynomial_coefficients(nb_data, 10, normalize=True)
    x = np.linspace(-1, 1, nb_data)
    order0 = np.ones(nb_data)
    order1 = x
    order2 = (3 * (x ** 2) - 1) / 2
    order3 = (5 * (x ** 3) - 3 * x) / 2
    order4 = (35 * (x ** 4) - 30 * (x ** 2) + 3) / 8
    order5 = (63 * (x ** 5) - 70 * (x ** 3) + 15 * x) / 8
    order6 = (231 * (x ** 6) - 315 * (x ** 4) + 105 * (x ** 2) - 5) / 16

    def error_is_below(approx, real, tol):
        return np.all(np.abs(approx - real) < (np.ptp(real) * tol))

    tolerance = 10 / nb_data
    assert np.allclose(p10[0], order0)
    assert np.allclose(p10[1], order1)
    assert error_is_below(p10[2], order2, tolerance)
    assert error_is_below(p10[3], order3, tolerance)
    assert error_is_below(p10[4], order4, tolerance)
    assert error_is_below(p10[5], order5, tolerance)
    assert error_is_below(p10[6], order6, tolerance)
