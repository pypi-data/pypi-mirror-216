"""Unit test file to test our Reader class.
"""
import os

from ultraspy.io.reader import Reader
from ultraspy.config import cfg


DATA_INFO_FIELDS = ['data_shape', 'data_type', 'is_iq']
ACQUISITION_INFO_FIELDS = ['sampling_freq', 't0', 'prf', 'signal_duration',
                           'delays', 'sound_speed']


def assert_is_a_valid_reader(reader):
    # Test if a reader has the good format
    assert reader.data_info
    assert reader.acquisition_info
    assert reader.probe
    for info in DATA_INFO_FIELDS:
        assert info in reader.data_info.keys()
    assert reader.data is not None
    for info in ACQUISITION_INFO_FIELDS:
        assert info in reader.acquisition_info.keys()
    assert reader.probe.geometry is not None
    assert reader.probe.central_freq is not None
    data_shape = reader.data.shape
    assert data_shape[1] == reader.acquisition_info['delays'].shape[0]
    assert data_shape[2] == reader.probe.geometry[0].size


def test_reader():
    # Test few examples files we stored in the resources
    rsc_dir = cfg.PATHS_RESOURCES
    picmus_data = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    must_data = os.path.join(rsc_dir, 'rotating_disk.mat')
    pa2_data = os.path.join(rsc_dir, 'pa2_wire.mat')
    assert_is_a_valid_reader(Reader(picmus_data, 'picmus'))
    assert_is_a_valid_reader(Reader(must_data, 'must'))
    assert_is_a_valid_reader(Reader(pa2_data, 'dbsas'))
