"""Unit test file to test our Beamformer class.
"""
import os
import pytest
import numpy as np

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.beamformer import Beamformer
from ultraspy.beamformers.das import DelayAndSum
from ultraspy.beamformers.pdas import PDelayAndSum
from ultraspy.beamformers.fdmas import FilteredDelayMultiplyAndSum
from ultraspy.config import cfg
import ultraspy as us


def test_initialization():
    # Test the default initialization
    beamformer = Beamformer(on_gpu=False)
    for info in ['emitted_probe', 'received_probe',
                 'emitted_thetas', 'received_thetas', 'delays',
                 'sound_speed', 'f_number',
                 't0', 'signal_duration',
                 'sampling_freq', 'central_freq', 'bandwidth', 'prf']:
        assert info in beamformer.setups.keys()


def test_init_using_beamformer():
    # Test if Picmus has been loaded properly
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    reader = Reader(picmus, 'picmus')
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer2 = PDelayAndSum(on_gpu=False)
    beamformer2.init_from_beamformer(beamformer)
    assert np.allclose(beamformer.setups['f_number'],
                       beamformer2.setups['f_number'])

    beamformer2.update_setup('f_number', 4.)
    assert len(beamformer2.setups['f_number']) == 2
    assert beamformer2.setups['f_number'][1] == 4.
    assert not np.allclose(beamformer.setups['f_number'],
                           beamformer2.setups['f_number'])

    beamformer3 = FilteredDelayMultiplyAndSum(on_gpu=False)
    beamformer3.init_from_beamformer(beamformer2)
    assert beamformer2.options['reduction'] == beamformer3.options['reduction']


def test_beamformer_calls():
    beamformer = Beamformer(on_gpu=False)
    scan = GridScan(np.linspace(-2, 2, 5), np.linspace(1, 9, 9))
    # We shouldn't use the parent class
    with pytest.raises(NotImplementedError):
        beamformer.beamform(np.zeros((2, 3, 10)), scan)
    with pytest.raises(NotImplementedError):
        beamformer.beamform_packet(np.zeros((5, 2, 3, 10)), scan)


def test_picmus_setup():
    # Test if Picmus has been loaded properly
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    reader = Reader(picmus, 'picmus')
    beamformer = Beamformer(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

    assert beamformer.setups['emitted_probe'].shape == (3, 75, 128)
    assert beamformer.setups['t0'] == 0


def test_envelope():
    # TODO: Should test the envelope using CPU on both methods (hilbert and
    #       demodulation), check if they are similar and if they perform as
    #       expected on Picmus data
    # TODO: Also test ValueError if the envelope hasn't been computed before
    pass


def test_beamform_packet():
    # Makes sure the beamform packet works as the frame by frame version
    rsc_dir = cfg.PATHS_RESOURCES
    disk = os.path.join(rsc_dir, 'rotating_disk.mat')
    reader = Reader(disk, 'must')
    x = np.linspace(-12.5, 12.5, 250) * 1e-3
    z = np.linspace(10, 35, 250) * 1e-3
    scan = GridScan(x, z, on_gpu=False)

    # Beamformers
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

    # Get 5 frames of data, enough for testing
    data = reader.data[:5, :]
    packet_size = data.shape[0]

    beamformed_packet = beamformer.beamform_packet(data, scan)

    for frame in range(packet_size):
        beamformed_frame = beamformer.beamform(data[frame], scan)
        assert np.allclose(beamformed_frame, beamformed_packet[..., frame])

    # Same tests on I/Qs
    beamformer.set_is_iq(True)
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0)

    # Beamform everything
    beamformed_packet = beamformer.beamform_packet(iqs, scan)

    for frame in range(iqs.shape[0]):
        beamformed_frame = beamformer.beamform(iqs[frame], scan)
        assert np.allclose(beamformed_frame, beamformed_packet[..., frame])


def test_beamform_packet_3d():
    # TODO: Should test once we'll have a packet of 3D data
    pass


def test_get_focused_data():
    # Test the function to only get delays based on a pixel
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    reader = Reader(picmus, 'picmus')
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

    delays = beamformer.get_focused_data((5e-3, 20e-3))
    assert np.sum(delays[0, :] > 0) == 67
    assert delays[25, 100] == pytest.approx(550.7929077148438)

    delays = beamformer.get_focused_data((-10e-3, 10e-3))
    assert np.sum(delays[0, :] > 0) == 33
    assert delays[70, 13] == pytest.approx(-1)
    assert delays[70, 14] == pytest.approx(253.3109130859375)


def test_get_focused_data_sta():
    # Test the function to only get delays based on a pixel
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'pa2_sta.mat'), 'dbsas')
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('sound_speed', 1440)
    beamformer.update_option('reduction', 'sum')

    # Only select a few transmissions, for faster computation
    beamformer.update_setup('transmissions_idx', list(range(0, 128, 8)))

    # Delays
    delays = beamformer.get_focused_data((10e-3, 45e-3))
    assert np.sum(delays[0, :] > 0) == 0
    assert np.sum(delays[8, :] > 0) == 106
    assert delays[8, 100] == pytest.approx(3164.9226)

    delays = beamformer.get_focused_data((-10e-3, 30e-3))
    assert np.sum(delays[0, :] > 0) == 81
    assert delays[3, 80] == pytest.approx(2209.4377)
    assert delays[3, 81] == pytest.approx(-1)


def test_get_focused_data_3d():
    # Test the get delays, if it is correct on a simple use
    beamformer = Beamformer(on_gpu=False)
    x_axis = np.linspace(-10e-3, 10e-3, 200)
    y_axis = np.linspace(-2e-3, 2e-3, 200)
    xx, yy = np.meshgrid(x_axis, y_axis)
    probe_3d = np.concatenate([xx.flatten()[None, :],
                               yy.flatten()[None, :],
                               np.zeros(xx.size)[None, :]])
    beamformer.update_setup('delays', np.zeros((1, probe_3d.shape[1])))
    beamformer.update_setup('emitted_probe', probe_3d[:, None])
    beamformer.update_setup('received_probe', probe_3d[:, None])
    beamformer.update_setup('emitted_thetas', np.zeros((1, probe_3d.shape[1])))
    beamformer.update_setup('received_thetas', np.zeros((1, probe_3d.shape[1])))
    beamformer.transmissions_indices = np.arange(1)
    beamformer.update_setup('f_number', 1.75)
    beamformer.update_setup('t0', 0)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('sampling_freq', 50e6)

    indices = beamformer.get_focused_data((0, 0, 10e-3))
    assert np.max(indices[0]) == pytest.approx(667.729)

    indices = beamformer.get_focused_data((-3e-3, 1e-3, 10e-3))
    assert np.max(indices[0]) == pytest.approx(674.6334)
