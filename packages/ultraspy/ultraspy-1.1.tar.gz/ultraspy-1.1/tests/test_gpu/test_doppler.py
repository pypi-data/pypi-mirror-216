"""Unit test file for testing the Doppler methods.
"""
import os
import numpy as np
import pytest

from ultraspy.gpu import gpu_utils
import ultraspy as us


def test_mean_wall_filter_gpu_equals_cpu(small_array_3d_complex):
    # Test mean wall filter
    d_data = gpu_utils.send_to_gpu(small_array_3d_complex, np.complex64)
    us.apply_wall_filter(d_data, 'mean')
    cpu_last = us.cpu.apply_wall_filter(small_array_3d_complex, 'mean')
    tol = 1e-6 * (small_array_3d_complex.shape[-1] + 1)
    assert (np.abs(d_data.get() - cpu_last) < tol).all()


def test_poly_wall_filter_gpu_equals_cpu(iqs_sample):
    # Compares the CPU and GPU implementations to make sure they are similar on
    # regular data (..., nb_f)
    degree = 3

    # CPU
    f_iqs_cpu = us.cpu.apply_wall_filter(iqs_sample.copy(), 'poly', degree)

    # GPU
    d_iqs = gpu_utils.send_to_gpu(iqs_sample.copy(), np.complex64)
    us.apply_wall_filter(d_iqs, 'poly', degree)
    f_iqs_gpu = d_iqs.get()

    # This is weird to have such a 'big' gap, but it could be explained by the
    # single / double precision I guess...?
    assert np.allclose(f_iqs_cpu, f_iqs_gpu, atol=1e-02)


def mean_difference_is_below(data1, data2, percentage):
    # Arbitrary assertion, we consider it's not so important to test the first
    # and last elements as they depend on the algorithm used for initial
    # conditions. Also, we want to keep uncertainty lower than 5% of the
    # extremes of our filtered signals.
    threshold = max(np.max(np.abs(data1)), np.max(np.abs(data2))) * percentage
    return np.mean(np.abs(data1 - data2)[..., 5:-5]) < threshold


def test_hp_filter_gpu_equals_cpu(iqs_sample):
    # Compares the CPU and GPU implementations to make sure they are similar on
    # regular data (nb_f, ...)
    degree = 3

    # CPU
    f_iqs_cpu = us.cpu.apply_wall_filter(iqs_sample.copy(), 'hp_filter', degree)

    # GPU
    d_iqs = gpu_utils.send_to_gpu(iqs_sample.copy(), np.complex64)
    us.apply_wall_filter(d_iqs, 'hp_filter', degree)
    f_iqs_gpu = d_iqs.get()

    assert mean_difference_is_below(f_iqs_cpu, f_iqs_gpu, 5 / 100)


def test_spatial_smoothing_cpu_equals_gpu():
    # Test in an ones matrix, the smoothing should then be homogeneous. It will
    # also be tested on a real example below (doppler maps)
    data = np.ones((10, 20))
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    k = 3
    result = us.cpu.spatial_smoothing(data, k)
    us.spatial_smoothing(d_data, k)
    assert np.allclose(result, d_data.get())


def test_median_smoothing():
    if os.getenv('ULTRASPY_GPU_LIB') == 'pycuda':
        d_data = gpu_utils.send_to_gpu(np.random.randn(10, 20), np.float32)
        with pytest.raises(NotImplementedError) as e:
            us.spatial_smoothing(d_data, 3, 'median')
    else:
        # Test the float version
        some_data = np.random.randn(10, 20)
        k = 3
        d_data = gpu_utils.send_to_gpu(some_data, np.float32)
        result = us.cpu.spatial_smoothing(some_data, k, 'median')
        us.spatial_smoothing(d_data, k, 'median')
        assert np.allclose(result, d_data.get())

        # Test the complex version
        some_data = np.random.randn(10, 20) + 1j * np.random.randn(10, 20)
        k = 3
        d_data = gpu_utils.send_to_gpu(some_data, np.complex64)
        result = us.cpu.spatial_smoothing(some_data, k, 'median')
        us.spatial_smoothing(d_data, k, 'median')
        assert np.allclose(result, d_data.get())


def test_color_map_doppler_gpu_equals_cpu(iqs_sample):
    # Checks if the GPU method is equivalent to the CPU, which has been tested
    # independently above
    sound_speed = 1540
    prf = 1000
    central_freq = 5e6
    nyq = sound_speed * prf / (4 * central_freq)

    # CPU
    color_map_cpu = us.cpu.get_color_doppler_map(
        iqs_sample.copy(), nyq, smoothing='hamming', kernel=5)

    # GPU
    d_iqs = gpu_utils.send_to_gpu(iqs_sample.copy(), np.complex64)
    d_color_map_gpu = us.get_color_doppler_map(d_iqs, nyq, smoothing='hamming',
                                               kernel=5)
    color_map_gpu = d_color_map_gpu.get()

    # Compare color maps
    assert np.allclose(color_map_cpu, color_map_gpu)


def test_power_map_doppler_gpu_equals_cpu(iqs_sample):
    # Checks if the GPU method is equivalent to the CPU, which has been tested
    # independently above
    # CPU
    power_map_cpu = us.cpu.get_power_doppler_map(iqs_sample.copy(),
                                                 smoothing='hamming', kernel=5)

    # GPU
    d_iqs = gpu_utils.send_to_gpu(iqs_sample.copy(), np.complex64)
    d_power_map_gpu = us.get_power_doppler_map(d_iqs, smoothing='hamming',
                                               kernel=5)
    power_map_gpu = d_power_map_gpu.get()

    # Compare color maps
    assert np.allclose(power_map_cpu, power_map_gpu, atol=1e-5)
