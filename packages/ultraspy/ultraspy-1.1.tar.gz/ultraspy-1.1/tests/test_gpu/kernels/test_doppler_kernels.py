"""Unit test file for all the Cuda kernels used in Doppler.
"""
import numpy as np

from ultraspy.gpu import gpu_utils
from ultraspy.gpu.kernels.doppler_kernels import (k_mean_wall_filter,
                                                  k_poly_wall_filter,
                                                  k_correlation_matrix,
                                                  k_color_map,
                                                  k_power_map)


def test_mean_wall_filter(array_xd_complex):
    # Tries the regular version, which has data of shape (..., nb_f)
    data = array_xd_complex.astype(np.complex64)
    nb_x = int(np.prod(data.shape[:-1]))
    nb_f = data.shape[-1]
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_x)
    k_mean_wall_filter(g_dim, b_dim, (d_data, np.uint32(nb_f), np.uint32(nb_x)))

    gpu_mean_wall_filter = d_data.get()
    cpu_mean_wall_filter = data - np.mean(data, axis=-1)[..., None]

    tol = 1e-6 * nb_f
    assert np.max(np.abs(gpu_mean_wall_filter - cpu_mean_wall_filter)) < tol


def test_poly_wall_filter(array_xd_complex):
    # Tries the regular version, which has data of shape (..., nb_f)
    data = array_xd_complex.astype(np.complex64)
    nb_x = int(np.prod(data.shape[:-1]))
    nb_f = data.shape[-1]
    deg = 5
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    d_polys = gpu_utils.initialize_empty((deg + 1, nb_f), np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_x)
    k_poly_wall_filter(g_dim, b_dim, (d_data, d_polys, np.uint32(deg),
                                      np.uint32(nb_f), np.uint32(nb_x)))
    gpu_poly_wall_filter = d_data.get()

    # Not so sure what to test here, we've made sure it can compile and run,
    # but it would be good to compare it with a CPU version of this polynomial
    # wall filter -> will be done while testing the main polynomial wall
    # filters instead of the kernels.
    assert gpu_poly_wall_filter is not None


def test_correlation_matrix(small_array_3d_complex):
    # Test on a simple 3D complex array, should be performed over last
    # dimension
    data = small_array_3d_complex.astype(np.complex64)
    nb_x = int(np.prod(data.shape[:-1]))
    nb_f = data.shape[-1]
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    d_correlation_matrix = gpu_utils.initialize_empty(data.shape[:-1],
                                                      np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_x)
    k_correlation_matrix(g_dim, b_dim,
                         (d_data, d_correlation_matrix,
                          np.uint32(nb_f), np.uint32(nb_x)))

    gpu_correlation_matrix = d_correlation_matrix.get()
    cpu_correlation_matrix = np.sum(data[..., :-1] * np.conj(data[..., 1:]),
                                    axis=-1)

    assert np.allclose(gpu_correlation_matrix, cpu_correlation_matrix)


def test_color_map(small_array_2d_complex):
    # Test on a simple 2D complex array with random nyquist velocity
    some_nyq = np.random.rand()
    data = small_array_2d_complex.astype(np.complex64)
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_color_map(g_dim, b_dim,
                (d_data, np.float32(some_nyq), np.uint32(data.size)))

    gpu_color_map = d_data.real.astype(np.float32).get()
    cpu_color_map = -some_nyq * np.imag(np.log(data)) / np.pi

    assert np.allclose(gpu_color_map, cpu_color_map)


def test_power_map(small_array_3d_complex):
    # Test on a simple 3D complex array, should be performed over last
    # dimension
    data = small_array_3d_complex.astype(np.complex64)
    nb_x = int(np.prod(data.shape[:-1]))
    nb_f = data.shape[-1]
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    d_power_map = gpu_utils.initialize_empty(data.shape[:-1], np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_x)
    k_power_map(g_dim, b_dim,
                (d_data, d_power_map, np.uint32(nb_f), np.uint32(nb_x)))

    gpu_power_map = d_power_map.get()
    cpu_power_map = np.mean(np.abs(data) ** 2, axis=-1)

    assert np.allclose(gpu_power_map, cpu_power_map)
