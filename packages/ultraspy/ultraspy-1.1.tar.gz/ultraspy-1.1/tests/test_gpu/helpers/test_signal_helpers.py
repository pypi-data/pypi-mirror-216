"""Unit test file for all the helpers used in Signal.
"""
import numpy as np
import scipy.signal

from ultraspy.helpers.signal_helpers import (get_filter_initial_conditions,
                                             filtfilt_routine)


def test_get_filter_initial_conditions():
    # Arguments, simple filter example
    order = 5
    b, a = scipy.signal.butter(order, 0.2, 'high')

    # Initial conditions
    new_b = get_filter_initial_conditions(order, a, b)

    # Inspired from Zhanping code, would be better to have a better check, but
    # this is all I have for now
    sol = np.array([1.77329024, -2.78596378, 1.76952449,
                    -0.10374317, -0.35416418])
    assert np.allclose(new_b, sol)


def test_filtfilt_routine():
    # This is properly tested in a higher level, in test_signal.py.
    assert filtfilt_routine
