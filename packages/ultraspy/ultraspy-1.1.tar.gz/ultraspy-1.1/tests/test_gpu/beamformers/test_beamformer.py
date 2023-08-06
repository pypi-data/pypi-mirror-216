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
from ultraspy.gpu import gpu_utils
from ultraspy.config import cfg
import ultraspy as us


def test_beamform_packet_3d():
    rsc_dir = cfg.PATHS_RESOURCES
    disk = os.path.join(rsc_dir, 'rotating_disk.mat')
    reader = Reader(disk, 'must')
    x = np.linspace(-12.5, 12.5, 200) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(10, 35, 300) * 1e-3
    scan = GridScan(x, y, z)

    # Beamformers
    beamformer = DelayAndSum(is_iq=True)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

    # Test a few frames on I/Qs
    info = beamformer.setups
    iqs = us.cpu.rf2iq(reader.data[:5], info['central_freq'],
                       info['sampling_freq'], beamformer.t0)

    # Send to GPU
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)

    # Beamform everything
    d_beamformed_packet = beamformer.beamform_packet(d_iqs, scan)
    beamformed_packet = d_beamformed_packet.get()

    for frame in range(iqs.shape[0]):
        d_frame = gpu_utils.send_to_gpu(iqs[frame].copy(), np.complex64)
        d_beamformed_frame = beamformer.beamform(d_frame, scan)
        beamformed_frame = d_beamformed_frame.get()
        assert np.allclose(beamformed_frame, beamformed_packet[..., frame])


def test_initialization():
    # Test the default initialization
    beamformer = Beamformer()
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
    beamformer = DelayAndSum()
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer2 = PDelayAndSum()
    beamformer2.init_from_beamformer(beamformer)
    assert np.allclose(beamformer.setups['f_number'].get(),
                       beamformer2.setups['f_number'].get())

    beamformer2.update_setup('f_number', 4.)
    assert len(beamformer2.setups['f_number']) == 2
    assert beamformer2.setups['f_number'].get()[1] == 4.
    assert not np.allclose(beamformer.setups['f_number'].get(),
                           beamformer2.setups['f_number'].get())

    beamformer3 = FilteredDelayMultiplyAndSum()
    beamformer3.init_from_beamformer(beamformer2)
    assert beamformer2.options['reduction'] == beamformer3.options['reduction']


def test_beamformer_calls():
    beamformer = Beamformer()
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
    beamformer = Beamformer()
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

    assert beamformer.setups['emitted_probe'].shape == (3, 75, 128)
    assert beamformer.setups['t0'] == 0


def test_envelope_gpu_equals_cpu():
    # Test envelope on Picmus
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    reader = Reader(picmus, 'picmus')
    x = np.linspace(-18, 18, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)

    d_data = gpu_utils.send_to_gpu(reader.data[0], np.float32)

    ref_beamformer = DelayAndSum(on_gpu=False)
    beamformer = DelayAndSum()
    ref_beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    d_beamformed = beamformer.beamform(d_data, scan)

    ref_envelope = ref_beamformer.compute_envelope(d_beamformed.get(), scan)
    envelope = beamformer.compute_envelope(d_beamformed, scan)
    # Might need to check why this is 1e-4, tolerance should be lower
    tol = 1e-4 * z.size
    assert np.allclose(ref_envelope, envelope.get(), atol=tol)


def test_beamform_packet():
    rsc_dir = cfg.PATHS_RESOURCES
    disk = os.path.join(rsc_dir, 'rotating_disk.mat')
    reader = Reader(disk, 'must')
    x = np.linspace(-12.5, 12.5, 200) * 1e-3
    z = np.linspace(10, 35, 300) * 1e-3
    scan = GridScan(x, z)

    # Beamformers
    beamformer = DelayAndSum()
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

    # Send to GPU and convert data to I/Qs
    d_data = gpu_utils.send_to_gpu(reader.data, np.float32)

    # Beamform everything
    d_beamformed_packet = beamformer.beamform_packet(d_data, scan)
    beamformed_packet = d_beamformed_packet.get()

    for frame in range(reader.data.shape[0]):
        d_frame = gpu_utils.send_to_gpu(reader.data[frame], np.float32)
        d_beamformed_frame = beamformer.beamform(d_frame, scan)
        beamformed_frame = d_beamformed_frame.get()
        assert np.allclose(beamformed_frame, beamformed_packet[..., frame])

    # Same tests on I/Qs
    beamformer.set_is_iq(True)
    d_data = gpu_utils.send_to_gpu(reader.data, np.complex64)
    info = beamformer.setups
    us.rf2iq(d_data, info['central_freq'], info['sampling_freq'], beamformer.t0)

    # Beamform everything
    d_beamformed_packet = beamformer.beamform_packet(d_data, scan)
    beamformed_packet = d_beamformed_packet.get()

    for frame in range(reader.data.shape[0]):
        d_beamformed_frame = beamformer.beamform(d_data[frame], scan)
        beamformed_frame = d_beamformed_frame.get()
        assert np.allclose(beamformed_frame, beamformed_packet[..., frame])
