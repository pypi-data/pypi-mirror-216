"""Fixtures for testing, mainly some random data generation of different
shapes / types for exhaustive testings.
"""
import os
from enum import Enum
import pytest
import numpy as np
import h5py
import scipy.io


class Types(Enum):
    INT = np.dtype('int32')
    FLOAT = np.dtype('float32')
    COMPLEX = np.dtype('complex64')


SMALL_ARRAY_1D_SHAPE = (5,)
BIG_ARRAY_1D_SHAPE = (10000,)
SMALL_ARRAY_2D_SHAPE = (4, 5)
BIG_ARRAY_2D_SHAPE = (1000, 1000)
SMALL_ARRAY_3D_SHAPE = (4, 6, 5)
SMALL_ARRAY_5D_SHAPE = (3, 2, 4, 1, 5)

SIGNAL_3D_SHAPE = (40, 50, 1000)

RANDOM_NB_DIMS_LIMIT = 5
RANDOM_DIMS_LIMIT = 10


def generate_data_of_shape(data_shape, d_type):
    # Generates an array of a given shape filled with random values, can be
    # complex (default), or float. Values between 0 and 1. If we chose to do it
    # with integers, it'll be rounded between 0 and 100.
    n = int(np.prod(data_shape))
    data = np.random.rand(n).reshape(*data_shape)
    if d_type == Types.COMPLEX:
        data = data + 1j * np.random.rand(n).reshape(*data_shape)
    elif d_type == Types.INT:
        data = np.round(data * 100)
    return data.copy()


def generate_data_of_random_shape(nb_dims_limit, shape_limit, d_type):
    # Generate a set of data with a random shape (random number of dims, up to
    # nb_dims_limit, each dimension up to shape_limit)
    nb_dims = np.random.randint(nb_dims_limit) + 1
    dims = [np.random.randint(shape_limit) + 1 for _ in range(nb_dims)]
    return generate_data_of_shape(dims, d_type)


def generate_signals(data_shape, sampling_rate, central_freq, d_type):
    # Creates a random signal, centered at a given frequency. The time samples
    # are along the last axis
    nb_x = int(np.prod(data_shape[:-1]))
    nb_z = data_shape[-1]
    time_step = 1 / sampling_rate
    x = np.linspace(0, (nb_z - 1) * time_step, nb_z)
    y = np.zeros((nb_x, nb_z))
    if d_type == Types.COMPLEX:
        y = y.astype(np.complex64)
    for i in range(nb_x):
        for _ in range(10):
            freq = (np.random.randn() * 10e6) + central_freq
            y[i, :] += np.sin(2 * np.pi * freq * x)
        if d_type == Types.COMPLEX:
            y[i, :] = y[i, :] * np.exp(2j * np.pi * central_freq * x)

    return y.reshape(data_shape).copy()


@pytest.fixture()
def small_array_1d_int():
    return generate_data_of_shape(SMALL_ARRAY_1D_SHAPE, Types.INT)
@pytest.fixture()
def small_array_1d_float():
    return generate_data_of_shape(SMALL_ARRAY_1D_SHAPE, Types.FLOAT)
@pytest.fixture()
def small_array_1d_complex():
    return generate_data_of_shape(SMALL_ARRAY_1D_SHAPE, Types.COMPLEX)


@pytest.fixture()
def big_array_1d_int():
    return generate_data_of_shape(BIG_ARRAY_1D_SHAPE, Types.INT)
@pytest.fixture()
def big_array_1d_float():
    return generate_data_of_shape(BIG_ARRAY_1D_SHAPE, Types.FLOAT)
@pytest.fixture()
def big_array_1d_complex():
    return generate_data_of_shape(BIG_ARRAY_1D_SHAPE, Types.COMPLEX)


@pytest.fixture()
def small_array_2d_int():
    return generate_data_of_shape(SMALL_ARRAY_2D_SHAPE, Types.INT)
@pytest.fixture()
def small_array_2d_float():
    return generate_data_of_shape(SMALL_ARRAY_2D_SHAPE, Types.FLOAT)
@pytest.fixture()
def small_array_2d_complex():
    return generate_data_of_shape(SMALL_ARRAY_2D_SHAPE, Types.COMPLEX)


@pytest.fixture()
def big_array_2d_int():
    return generate_data_of_shape(BIG_ARRAY_2D_SHAPE, Types.INT)
@pytest.fixture()
def big_array_2d_float():
    return generate_data_of_shape(BIG_ARRAY_2D_SHAPE, Types.FLOAT)
@pytest.fixture()
def big_array_2d_complex():
    return generate_data_of_shape(BIG_ARRAY_2D_SHAPE, Types.COMPLEX)


@pytest.fixture()
def small_array_3d_int():
    return generate_data_of_shape(SMALL_ARRAY_3D_SHAPE, Types.INT)
@pytest.fixture()
def small_array_3d_float():
    return generate_data_of_shape(SMALL_ARRAY_3D_SHAPE, Types.FLOAT)
@pytest.fixture()
def small_array_3d_complex():
    return generate_data_of_shape(SMALL_ARRAY_3D_SHAPE, Types.COMPLEX)


@pytest.fixture()
def small_array_5d_int():
    return generate_data_of_shape(SMALL_ARRAY_5D_SHAPE, Types.INT)
@pytest.fixture()
def small_array_5d_float():
    return generate_data_of_shape(SMALL_ARRAY_5D_SHAPE, Types.FLOAT)
@pytest.fixture()
def small_array_5d_complex():
    return generate_data_of_shape(SMALL_ARRAY_5D_SHAPE, Types.COMPLEX)


@pytest.fixture()
def array_xd_int():
    return generate_data_of_random_shape(
                        RANDOM_NB_DIMS_LIMIT, RANDOM_DIMS_LIMIT, Types.INT)
@pytest.fixture()
def array_xd_float():
    return generate_data_of_random_shape(
                        RANDOM_NB_DIMS_LIMIT, RANDOM_DIMS_LIMIT, Types.FLOAT)
@pytest.fixture()
def array_xd_complex():
    return generate_data_of_random_shape(
                        RANDOM_NB_DIMS_LIMIT, RANDOM_DIMS_LIMIT, Types.COMPLEX)


@pytest.fixture()
def iqs_sample():
    rsc_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
    return scipy.io.loadmat(os.path.join(rsc_dir, 'iqs_doppler.mat'))['iqs']


@pytest.fixture()
def rfs_simu_picmus():
    rsc_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
    f = h5py.File(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'r')
    shortcut = f['US']['US_DATASET0000']
    return {
        'data': np.array(shortcut['data']['real']),
        'angles': np.array(shortcut['angles']),
        'geometry': np.array(shortcut['probe_geometry'][0]),
        'sampling_frequency': shortcut['sampling_frequency'][0],
        'central_freq': shortcut['sampling_frequency'][0] / 4,
        't0': shortcut['initial_time'][0],
        'f_number': 1.75,
        'prf': shortcut['PRF'][0],
        'is_iq': False,
        'sound_speed': shortcut['sound_speed'][0],
    }


@pytest.fixture()
def fake_3d_signals_5mhz_float():
    return generate_signals(SIGNAL_3D_SHAPE, 50e6, 5e6, Types.FLOAT)
@pytest.fixture()
def fake_3d_signals_5mhz_complex():
    return generate_signals(SIGNAL_3D_SHAPE, 50e6, 5e6, Types.COMPLEX)
