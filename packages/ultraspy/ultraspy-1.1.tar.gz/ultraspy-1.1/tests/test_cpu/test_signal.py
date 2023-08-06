"""Unit test file for testing the Signal methods.
"""
import numpy as np
import scipy.signal
import pytest

from ultraspy.cpu import down_mix, matched_filter, rf2iq, normalize, filtfilt


def test_down_mix(small_array_5d_float):
    # Super high level test, but this method is used within RF2IQ, which is
    # more heavily tested later (comparison with MUST results).
    down_mixed = down_mix(small_array_5d_float, 5e6, 20e6, 0, -1)
    assert down_mixed.imag.any()


def test_down_mix_shapes(small_array_5d_float):
    # Test the down-mixing on different axes.
    fs = 20e6
    f0 = 5e6
    t0 = 1e-6
    axis = np.random.randint(5)
    down_mixed = down_mix(small_array_5d_float, f0, fs,  t0, axis)
    transposed = np.moveaxis(small_array_5d_float, axis, -1)
    down_mixed_2 = down_mix(transposed, f0, fs, t0, -1)
    down_mixed_2 = np.moveaxis(down_mixed_2, -1, axis)
    assert np.allclose(down_mixed, down_mixed_2)


def test_rf2iq(rfs_simu_picmus):
    # Comparison of the RF2IQ method on the PICMUS dataset obtained with MUST.
    # For the min, max and median, we are comparing real and imaginary parts as
    # the comparison operators (< / >) are not the same in matlab and python
    must_raw_values = {
        'min_real': -1.014184987078125,
        'min_imag': -1.015260428667955,
        'max_real': 1.024821972413710,
        'max_imag': 1.022328317902549,
        'median_real': 2.822957834796692e-67,
        'median_imag': -1.199033642966317e-67,
        'mean': 3.971650903869870e-05 - 5.764961274402035e-05j,
    }

    # Information from data
    fs = rfs_simu_picmus['sampling_frequency']
    f0 = rfs_simu_picmus['central_freq']
    t0 = rfs_simu_picmus['t0']
    data = rfs_simu_picmus['data']

    # Convert to I/Qs
    iqs = rf2iq(data, f0, fs, t0, bandwidth=200)

    assert must_raw_values['min_real'] == pytest.approx(np.min(iqs.real))
    assert must_raw_values['min_imag'] == pytest.approx(np.min(iqs.imag))
    assert must_raw_values['max_real'] == pytest.approx(np.max(iqs.real))
    assert must_raw_values['max_imag'] == pytest.approx(np.max(iqs.imag))
    assert must_raw_values['median_real'] == pytest.approx(np.median(iqs.real))
    assert must_raw_values['median_imag'] == pytest.approx(np.median(iqs.imag))
    assert must_raw_values['mean'] == pytest.approx(np.mean(iqs))


def test_rf2iq_t0(rfs_simu_picmus):
    # Comparison of the RF2IQ method on the PICMUS dataset obtained with MUST
    # with a different values of t0. For the min, max and median, we are
    # comparing real and imaginary parts as the comparison operators (< / >)
    # are not the same in matlab and python
    must_raw_values = {
        'min_real': -1.044319982040691,
        'min_imag': -1.052702422099564,
        'max_real': 1.037939453833216,
        'max_imag': 1.039066287562293,
        'median_real': 2.039264823378133e-60,
        'median_imag': -1.089547349498454e-57,
        'mean': 2.576637647971679e-05 + 6.509203317505495e-05j,
    }

    # Information from data
    fs = rfs_simu_picmus['sampling_frequency']
    fc = rfs_simu_picmus['central_freq']
    t0 = 32e-6  # Non-valid t0, for testing
    data = rfs_simu_picmus['data']

    # Convert to I/Qs
    iqs = rf2iq(data, fc, fs, t0, bandwidth=200)

    assert must_raw_values['min_real'] == pytest.approx(np.min(iqs.real))
    assert must_raw_values['min_imag'] == pytest.approx(np.min(iqs.imag))
    assert must_raw_values['max_real'] == pytest.approx(np.max(iqs.real))
    assert must_raw_values['max_imag'] == pytest.approx(np.max(iqs.imag))
    assert must_raw_values['median_real'] == pytest.approx(np.median(iqs.real))
    assert must_raw_values['median_imag'] == pytest.approx(np.median(iqs.imag))
    assert must_raw_values['mean'] == pytest.approx(np.mean(iqs))


def test_matched_filter():
    # Test a simple signal (one undulation, noised), match filtered with its
    # own non-noisy signal. It should return a signal looking like an arctan,
    # with its maximum value approximately centered in the filtered signal.
    t = np.linspace(0, 1, 100)
    sig = np.sin(2 * np.pi * t)
    noisy = sig + np.random.randn(len(sig))
    filtered = matched_filter(noisy, sig)
    assert abs(np.argmax(filtered) - len(sig) // 2) < 10
    filtered = matched_filter(sig, sig)
    assert np.argmax(filtered) == len(sig) // 2


def test_matched_filter_spectral_equals_time(fake_3d_signals_5mhz_float):
    # Make sure the time and spectral modes provide similar results
    sig_duration = 1e-6
    sampling_freq = 20e6
    central_freq = 5e6
    t = np.arange(0, sig_duration, 1 / sampling_freq)
    ref = np.sin(2 * np.pi * central_freq * t)
    filtered = matched_filter(fake_3d_signals_5mhz_float, ref)
    filtered_2 = matched_filter(fake_3d_signals_5mhz_float, ref, 'spectral')
    assert np.allclose(filtered, filtered_2)


def test_normalize(rfs_simu_picmus):
    # Basic tests for normalization
    normalized = normalize(rfs_simu_picmus['data'])
    assert (-1 <= normalized).all()
    assert (normalized <= 1).all()
    assert np.min(normalized) == -1 or np.max(normalized) == 1
    normalized = normalize(rfs_simu_picmus['data'], 45)
    assert np.allclose(normalized, rfs_simu_picmus['data'] / 45)


def test_filtfilt(fake_3d_signals_5mhz_float):
    cutoff = 8e6
    fs = 50e6

    # Make sure it is still equal to scipy in a basic example
    filtered_1 = filtfilt(fake_3d_signals_5mhz_float, cutoff, fs, 'high')
    w_n = cutoff / (fs / 2)
    b, a = scipy.signal.butter(5, w_n, 'high')
    filtered_2 = scipy.signal.filtfilt(b, a, fake_3d_signals_5mhz_float)
    assert np.allclose(filtered_1, filtered_2)

    # Other axis
    filtered_1 = filtfilt(fake_3d_signals_5mhz_float, cutoff, fs, 'low', axis=1)
    w_n = cutoff / (fs / 2)
    b, a = scipy.signal.butter(5, w_n, 'low')
    filtered_2 = scipy.signal.filtfilt(b, a, fake_3d_signals_5mhz_float, axis=1)
    assert np.allclose(filtered_1, filtered_2)

    # Out of bound w_n
    with pytest.raises(ValueError):
        filtfilt(fake_3d_signals_5mhz_float, 0, fs, 'low')
    with pytest.raises(ValueError):
        filtfilt(fake_3d_signals_5mhz_float, fs / 2, fs, 'low')
