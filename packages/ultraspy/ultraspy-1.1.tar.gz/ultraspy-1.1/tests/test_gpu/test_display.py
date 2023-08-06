"""Unit test file for testing the Display methods.
"""
import ultraspy as us


def test_convert_to_b_mode_equals_cpu():
    # Not so relevant to test anything, it is very straightforward
    assert us.to_b_mode
    assert us.cpu.to_b_mode
