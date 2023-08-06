"""Unit test file for testing the GPU utilities methods.
"""
import numpy as np

from ultraspy.gpu import gpu_utils


def are_valid_dimensions(b_dim, g_dim, nb_processes):
    # Check if they have only one dimension, and if all the operations can be
    # performed within the chosen architecture
    return np.squeeze(b_dim).ndim == 1 and \
           np.squeeze(g_dim).ndim == 1 and \
           np.prod(b_dim) * np.prod(g_dim) >= nb_processes


def test_compute_flat_grid_size():
    # Different sizes to process, regular one
    assert are_valid_dimensions(
        *gpu_utils.compute_flat_grid_size(5120, 1024), 5120)
    # Very few processes
    assert are_valid_dimensions(
        *gpu_utils.compute_flat_grid_size(1, 1024), 1)
    # Very Same number of processes
    assert are_valid_dimensions(
        *gpu_utils.compute_flat_grid_size(1024, 1024), 1024)


def test_send_to_gpu():
    # Check if data has been sent on GPU
    data = np.arange(100).reshape(5, 20).astype(np.float32)
    d_data = gpu_utils.send_to_gpu(data, data.dtype)
    assert d_data.shape == data.shape
    assert d_data.dtype == data.dtype
    assert np.allclose(d_data.get(), data)


def test_initialize_empty():
    # Check if data has been sent on GPU
    shp = (20, 10, 3)
    dtp = np.float32
    d_data = gpu_utils.initialize_empty(shp, dtp)
    assert d_data.shape == shp
    assert d_data.dtype == dtp


def test_set_values():
    # Check if data can properly been moved
    data = np.arange(100).reshape(5, 20).astype(np.float32)
    data2 = np.arange(100).reshape(5, 20).astype(np.float32) * -1
    d_data = gpu_utils.send_to_gpu(data, data.dtype)
    d_data2 = gpu_utils.send_to_gpu(data2, data2.dtype)
    gpu_utils.set_values(d_data, d_data2)
    assert np.allclose(d_data.get(), data2)
    assert np.allclose(d_data2.get(), data2)
