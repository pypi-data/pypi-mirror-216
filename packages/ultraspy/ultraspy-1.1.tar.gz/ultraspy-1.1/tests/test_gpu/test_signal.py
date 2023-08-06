"""Unit test file for testing the Signal methods.
"""
import pytest
import numpy as np

from ultraspy.gpu import gpu_utils
import ultraspy as us


def test_down_mix_gpu_equals_cpu(small_array_2d_float):
    # Arbitrary frequencies values
    fs, fc, t0 = 2000, 500, 0.02
    d_data = gpu_utils.send_to_gpu(small_array_2d_float, np.complex64)
    us.down_mix(d_data, fc, fs, t0)
    down_mixed_cpu = us.cpu.down_mix(small_array_2d_float, fc, fs, t0)
    assert np.allclose(d_data.get(), down_mixed_cpu)


def test_down_mix_inplace(small_array_2d_float):
    # Arbitrary frequencies values
    fs, fc, t0 = 2000, 500, 0.02
    d_data = gpu_utils.send_to_gpu(small_array_2d_float, np.complex64)
    d_output = us.down_mix(d_data, fc, fs, t0, inplace=False)
    assert np.allclose(d_data.get(), small_array_2d_float)
    us.down_mix(d_data, fc, fs, t0)
    assert np.allclose(d_data.get(), d_output.get())


def test_rf2iq_gpu_equals_cpu(rfs_simu_picmus):
    # Information from data
    fs = rfs_simu_picmus['sampling_frequency']
    fc = rfs_simu_picmus['central_freq']
    t0 = rfs_simu_picmus['t0']
    data = rfs_simu_picmus['data'].copy()

    # Compare
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    us.rf2iq(d_data, fc, fs, t0, bandwidth=100)
    gpu_result = d_data.get()
    cpu_result = us.cpu.rf2iq(data, fc, fs, t0, bandwidth=100)
    tol = 1e-6 * data.shape[-1]
    assert np.max(np.abs(gpu_result - cpu_result)) < tol


def test_rf2iq_inplace(rfs_simu_picmus):
    # Information from data
    fs = rfs_simu_picmus['sampling_frequency']
    fc = rfs_simu_picmus['central_freq']
    t0 = rfs_simu_picmus['t0']
    data = rfs_simu_picmus['data'].copy()

    # Arbitrary frequencies values
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    d_output = us.rf2iq(d_data, fc, fs, t0, bandwidth=100, inplace=False)
    assert np.allclose(d_data.get(), data)
    us.rf2iq(d_data, fc, fs, t0, bandwidth=100)
    assert np.allclose(d_data.get(), d_output.get())


def test_matched_filter_gpu_equals_cpu(fake_3d_signals_5mhz_float):
    # Perform match filter with a simple sine, centered at 5MHz
    t = np.linspace(0, 1 / 5e6, 100)
    ref_sig = np.sin(2 * np.pi * 5e6 * t)

    # Compare time domain
    d_data = gpu_utils.send_to_gpu(fake_3d_signals_5mhz_float, np.float32)
    us.matched_filter(d_data, ref_sig)
    gpu_result = d_data.get()
    cpu_result = us.cpu.matched_filter(fake_3d_signals_5mhz_float.copy(),
                                       ref_sig)
    tol = 1e-6 * len(t)
    assert np.max(np.abs(gpu_result - cpu_result)) < tol

    # Compare spatial domain
    # TODO: Not implemented yet


def test_matched_filter_inplace(fake_3d_signals_5mhz_float):
    # Perform match filter with a simple sine, centered at 5MHz
    t = np.linspace(0, 1 / 5e6, 100)
    ref_sig = np.sin(2 * np.pi * 5e6 * t)

    # Compare time domain
    d_data = gpu_utils.send_to_gpu(fake_3d_signals_5mhz_float, np.float32)
    d_output = us.matched_filter(d_data, ref_sig, inplace=False)
    assert np.allclose(d_data.get(), fake_3d_signals_5mhz_float)
    us.matched_filter(d_data, ref_sig)
    assert np.allclose(d_data.get(), d_output.get())


def test_normalize_gpu_equals_cpu(rfs_simu_picmus):
    data = rfs_simu_picmus['data'].copy()
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    us.normalize(d_data)
    gpu_result = d_data.get()
    cpu_result = us.cpu.normalize(data)

    assert np.allclose(gpu_result, cpu_result)


def test_normalize_inplace(rfs_simu_picmus):
    data = rfs_simu_picmus['data'].copy()
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    d_output = us.normalize(d_data, inplace=False)
    assert np.allclose(d_data.get(), data)
    us.normalize(d_data)
    assert np.allclose(d_data.get(), d_output.get())
