"""Unit test file for testing the Signal methods.
"""
import numpy as np

from ultraspy.gpu import gpu_utils
import ultraspy as us


def mean_difference_is_below(data1, data2, percentage):
    # Arbitrary assertion, we consider it's not so important to test the first
    # and last elements as they depend on the algorithm used for initial
    # conditions. Also, we want to keep uncertainty lower than 5% of the
    # extremes of our filtered signals.
    threshold = max(np.max(np.abs(data1)), np.max(np.abs(data2))) * percentage
    return np.mean(np.abs(data1 - data2)[..., 5:-5]) < threshold


def test_filtfilt_gpu_equals_cpu(iqs_sample):
    # Tolerance for single / double precision approximations is set to 5%
    tol = 5 / 100
    order, fs = 5, 25e6

    # HP and LP filters, tests on medium, low, high threshold
    for filter_type in ['low', 'high']:
        for f0 in [1.5e6, 3e6, 6e6, 8e6, 10e6]:
            data = iqs_sample.copy()
            d_data = gpu_utils.send_to_gpu(data, np.complex64)
            us.filtfilt(d_data, f0, fs, filter_type, order)
            gpu_result = d_data.get()
            cpu_result = us.cpu.filtfilt(data, f0, fs, filter_type, order)
            assert mean_difference_is_below(gpu_result, cpu_result, tol)


def test_filtfilt_real_data_adapted_shape(iqs_sample):
    # Some test to check if we can work with a GPUArray with any shape as long
    # as it has been reshaped
    data = iqs_sample.copy()
    fs = 25e6
    s1, s2, nb_z = data.shape

    # Some easy HP filter
    order, f0, filter_type = 5, 2.5e6, 'high'

    # GPU filtfilt with some reshaping of the GPUArray, but no transpose
    # (doesn't work)
    # TODO: Would be cool to add a transposing operation when we'll have a
    #       proper implementation
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    d_data = d_data.reshape(s1 * s2, nb_z)
    # d_data = d_data.transpose((1, 0))
    us.filtfilt(d_data, f0, fs, filter_type, order)
    # d_data = d_data.transpose((1, 0))
    d_data = d_data.reshape(s1, s2, nb_z)
    gpu_result = d_data.get()

    # Scipy filtfilt
    cpu_result = us.cpu.filtfilt(data, f0, fs, filter_type, order)

    # Check if they are close
    assert mean_difference_is_below(gpu_result, cpu_result, 5 / 100)


def test_filtfilt_simulated_data(fake_3d_signals_5mhz_float,
                                 fake_3d_signals_5mhz_complex):
    # Some easy HP filter
    fs = 25e6
    order, f0, filter_type = 5, 2.5e6, 'high'

    # Floats as complexes
    data = fake_3d_signals_5mhz_float.copy()
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    us.filtfilt(d_data, f0, fs, filter_type, order)
    gpu_result = d_data.get()
    cpu_result = us.cpu.filtfilt(data, f0, fs, filter_type, order)
    assert mean_difference_is_below(gpu_result, cpu_result, 5 / 100)

    # Complexes as complexes
    data = fake_3d_signals_5mhz_complex.copy()
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    us.filtfilt(d_data, f0, fs, filter_type, order)
    gpu_result = d_data.get()
    cpu_result = us.cpu.filtfilt(data, f0, fs, filter_type, order)
    assert mean_difference_is_below(gpu_result, cpu_result, 5 / 100)


def test_filtfilt_axes(fake_3d_signals_5mhz_float):
    # Some easy HP filter
    fs = 25e6
    order, f0, filter_type = 5, 2.5e6, 'high'

    # Floats as complexes
    data = fake_3d_signals_5mhz_float.copy()
    swapped_data = np.swapaxes(fake_3d_signals_5mhz_float, 1, -1).copy()
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    d_swapped = gpu_utils.send_to_gpu(swapped_data, np.complex64)
    us.filtfilt(d_data, f0, fs, filter_type, order)
    us.filtfilt(d_swapped, f0, fs, filter_type, order, axis=1)
    gpu_result = d_data.get()
    gpu_result_2 = d_swapped.get()
    gpu_result_2 = np.swapaxes(gpu_result_2, -1, 1)
    assert np.allclose(gpu_result, gpu_result_2)
