"""Unit test file for all the Cuda kernels used in Doppler.
"""
import numpy as np

from ultraspy.gpu import gpu_utils
from ultraspy.gpu.kernels.signal_kernels import (k_down_mix,
                                                 k_init_filter,
                                                 k_init_start_sig,
                                                 k_filter0,
                                                 k_init_end_sig)


def test_down_mix(small_array_2d_complex,
                  big_array_2d_complex):
    def try_down_mix(data):
        # We consider that the last dimension is the time samples, and use some
        # basic signal characteristics
        some_fs, some_fc, some_t0 = 20e6, 5e6, 2e-6
        nb_x = int(np.prod(data.shape[:-1]))
        nb_ts = data.shape[-1]
        d_data = gpu_utils.send_to_gpu(data, np.complex64)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
        k_down_mix(g_dim, b_dim,
                   (d_data, np.uint32(nb_ts), np.uint32(nb_x),
                    np.float32(some_t0),
                    np.float32(some_fc), np.float32(some_fs)))

        gpu_down_mix = d_data.get()
        t = np.arange(nb_ts) / some_fs + some_t0
        phase = np.exp(-2j * np.pi * some_fc * t)
        cpu_down_mix = data * phase[None, :]

        # Needs an increased tolerance here, as a dozen of operation has been
        # performed in double precision on CPU
        tol = nb_ts * 1e-6
        assert np.allclose(gpu_down_mix, cpu_down_mix, atol=tol)

    try_down_mix(small_array_2d_complex)
    try_down_mix(big_array_2d_complex)


def test_init_filter():
    # This function is part of a whole, a bit hard to test without explicit
    # data information, so I am not so sure what to test here.. It would be
    # good to compare it with a CPU version. This might be done and we will
    # also test the whole filtfilt method (which this function is a part of),
    # as a global test.
    assert k_init_filter


def test_init_start_sig():
    # This function is part of a whole, a bit hard to test without explicit
    # data information, so I am not so sure what to test here.. It would be
    # good to compare it with a CPU version. This might be done and we will
    # also test the whole filtfilt method (which this function is a part of),
    # as a global test.
    assert k_init_start_sig


def test_filter0():
    # This function is part of a whole, a bit hard to test without explicit
    # data information, so I am not so sure what to test here.. It would be
    # good to compare it with a CPU version. This might be done and we will
    # also test the whole filtfilt method (which this function is a part of),
    # as a global test.
    assert k_filter0


def test_init_end_sig():
    # This function is part of a whole, a bit hard to test without explicit
    # data information, so I am not so sure what to test here.. It would be
    # good to compare it with a CPU version. This might be done and we will
    # also test the whole filtfilt method (which this function is a part of),
    # as a global test.
    assert k_init_end_sig
