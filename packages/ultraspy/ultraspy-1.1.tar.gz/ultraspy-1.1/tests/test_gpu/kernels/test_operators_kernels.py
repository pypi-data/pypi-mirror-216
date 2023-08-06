"""Unit test file for all the operation Cuda kernels.
"""
import numpy as np
from scipy.signal import correlate as scipy_signal_correlate
from scipy.ndimage import correlate as scipy_nd_image_correlate

from ultraspy.gpu import gpu_utils
from ultraspy.gpu.kernels.operators_kernels import (k_by2,
                                                    k_divide_by,
                                                    k_flip,
                                                    k_flip_within,
                                                    k_get_modulo,
                                                    k_to_db,
                                                    k_convolve1d,
                                                    k_convolve2d,
                                                    k_max)


def test_data_by2(small_array_1d_int,
                  small_array_1d_float,
                  big_array_1d_float,
                  small_array_1d_complex):
    # Test complexes
    d_data = gpu_utils.send_to_gpu(small_array_1d_complex, np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_by2(g_dim, b_dim, (d_data, np.uint32(d_data.size)))
    assert np.allclose(d_data.get(), small_array_1d_complex * 2)

    # Test floats
    d_data = gpu_utils.send_to_gpu(small_array_1d_float, np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_by2(g_dim, b_dim, (d_data, np.uint32(d_data.size)))
    assert np.allclose(d_data.get(), small_array_1d_float * 2)

    # Test ints
    d_data = gpu_utils.send_to_gpu(small_array_1d_int, np.int32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_by2(g_dim, b_dim, (d_data, np.uint32(d_data.size)))
    assert np.allclose(d_data.get(), small_array_1d_int * 2)


def test_data_divide_by(small_array_1d_float,
                        small_array_1d_complex):
    # Test complexes
    d_data = gpu_utils.send_to_gpu(small_array_1d_complex, np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_divide_by(g_dim, b_dim, (d_data, np.float32(5), np.uint32(d_data.size)))
    cpu_sp = small_array_1d_complex.astype(np.complex64) / np.float32(5)
    assert np.allclose(d_data.get(), cpu_sp)

    # Test floats
    d_data = gpu_utils.send_to_gpu(small_array_1d_float, np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_divide_by(g_dim, b_dim, (d_data, np.float32(5), np.uint32(d_data.size)))
    cpu_sp = small_array_1d_float.astype(np.float32) / np.float32(5)
    assert np.allclose(d_data.get(), cpu_sp)


def test_data_get_max(small_array_1d_float,
                      small_array_2d_float):
    # Test different shapes
    d_data = gpu_utils.send_to_gpu(small_array_1d_float, np.float32)
    assert k_max(d_data) == np.max(small_array_1d_float.astype(np.float32))
    d_data = gpu_utils.send_to_gpu(small_array_2d_float, np.int32)
    cpu_max = np.max(small_array_2d_float.astype(np.int32))
    assert k_max(d_data) == cpu_max


def test_data_flip(small_array_2d_float,
                   small_array_2d_complex,
                   big_array_2d_float,
                   small_array_5d_float):
    def try_flip_data_of_dims(data, d_type):
        nb_x = data.shape[0]
        nb_z = int(np.prod(data.shape[1:]))
        d_data = gpu_utils.send_to_gpu(data, d_type)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
        k_flip(g_dim, b_dim, (d_data, np.uint32(nb_x), np.uint32(nb_z)))
        assert np.allclose(d_data.get(), np.flip(data, axis=0))

    # Different sizes to process
    try_flip_data_of_dims(small_array_2d_float, np.float32)
    try_flip_data_of_dims(small_array_2d_complex, np.complex64)
    try_flip_data_of_dims(big_array_2d_float, np.float32)
    try_flip_data_of_dims(small_array_5d_float, np.float32)


def test_data_flip_within(small_array_2d_float):
    # Considers the data_flip test was ok, so just make sure the original data
    # was not modified, and compare the result to data_flip
    data = small_array_2d_float.astype(np.float32)
    nb_x, nb_z = data.shape
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    d_flipped_data = gpu_utils.initialize_empty(data.shape, np.float32)
    k_flip_within(g_dim, b_dim,
                  (d_data, d_flipped_data, np.uint32(nb_x), np.uint32(nb_z)))

    # First assert d_data hasn't been changed
    assert np.allclose(d_data.get(), small_array_2d_float)

    # Then compare results
    k_flip(g_dim, b_dim, (d_data, np.uint32(nb_x), np.uint32(nb_z)))
    assert np.allclose(d_data.get(), d_flipped_data.get())


def test_get_modulo(small_array_2d_complex):
    # Test on a simple array
    data = small_array_2d_complex.astype(np.complex64)
    d_data = gpu_utils.send_to_gpu(data, np.complex64)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    d_modules = gpu_utils.initialize_empty(data.shape, np.float32)
    k_get_modulo(g_dim, b_dim, (d_data, np.uint32(data.size), d_modules))
    assert np.allclose(d_modules.get(), np.abs(data))


def test_to_db(big_array_1d_float):
    # Test on a simple array
    data = big_array_1d_float.astype(np.float32)
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_to_db(g_dim, b_dim, (d_data, np.uint32(data.size)))
    cpu_sp = 20 * np.log10(data)
    assert np.allclose(d_data.get(), cpu_sp)


def test_convolve1d(small_array_2d_float,
                    small_array_2d_complex,
                    small_array_1d_float):
    def try_to_convolve_this(data, k):
        nb_x = int(np.prod(data.shape[:-1]))
        nb_z = data.shape[-1]
        d_data = gpu_utils.send_to_gpu(data, data.dtype)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
        d_convolved = gpu_utils.initialize_empty(data.shape, data.dtype)
        d_kernel = gpu_utils.send_to_gpu(k, np.float32)
        k_convolve1d(g_dim, b_dim,
                     (d_data, d_convolved, d_kernel, np.uint32(nb_x),
                      np.uint32(nb_z), np.uint32(len(k)), np.uint32(data.size)))
        exp_k = k.reshape([1] * (len(data.shape) - 1) + [len(k)])
        cpu_sp = scipy_signal_correlate(data, exp_k, 'same')
        assert np.allclose(d_convolved.get(), cpu_sp)

    # Some random small kernel vector
    kernel = np.random.rand(3)

    # Different data shapes / types
    try_to_convolve_this(small_array_2d_float.astype(np.float32), kernel)
    try_to_convolve_this(small_array_2d_complex.astype(np.complex64), kernel)
    try_to_convolve_this(small_array_1d_float.astype(np.float32), kernel)


def test_convolve2d(small_array_2d_float,
                    small_array_2d_complex,
                    big_array_2d_float):
    def try_to_convolve_this(data, kernel, d_type):
        # CPU version
        convolved_cpu = scipy_nd_image_correlate(data, kernel, mode='nearest')

        # GPU version
        nb_x, nb_y = data.shape
        k_size, _ = kernel.shape
        d_data = gpu_utils.send_to_gpu(data, d_type)
        d_convolved = gpu_utils.initialize_empty(data.shape, d_type)
        d_kernel = gpu_utils.send_to_gpu(kernel, np.float32)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
        k_convolve2d(g_dim, b_dim,
                     (d_data, d_convolved, d_kernel, np.uint32(nb_x),
                      np.uint32(nb_y), np.uint32(k_size)))
        assert np.allclose(d_convolved.get(), convolved_cpu)

    # Some random small kernel vector
    small_kernel = np.random.rand(3 * 3).reshape(3, 3)
    big_kernel = np.random.rand(25, 25).reshape(25, 25)

    # Some random float data
    try_to_convolve_this(small_array_2d_float, small_kernel, np.float32)
    try_to_convolve_this(small_array_2d_complex, small_kernel, np.complex64)
    try_to_convolve_this(big_array_2d_float, big_kernel, np.float32)
