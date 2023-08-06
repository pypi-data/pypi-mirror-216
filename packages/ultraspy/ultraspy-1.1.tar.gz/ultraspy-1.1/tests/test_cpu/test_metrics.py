"""Unit test file for testing the Metrics methods.
"""
import os
import pytest
import numpy as np

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.das import DelayAndSum
from ultraspy.config import cfg
import ultraspy as us

from ultraspy.metrics import (get_most_salient_point,
                              find_signal_and_noise,
                              signal_noise_ratio,
                              get_full_width_at_half_maximum,
                              get_peak_side_lobe,
                              get_lobe_metrics,
                              build_mask,
                              get_contrat_noise_ratio)


def test_get_most_salient_point(small_array_2d_float,
                                small_array_2d_complex,
                                small_array_3d_float):
    nb_x, nb_y = small_array_2d_float.shape
    x = np.random.randint(nb_x)
    y = np.random.randint(nb_y)
    small_array_2d_float[x, y] = np.max(small_array_2d_float) + 1
    assert get_most_salient_point(small_array_2d_float) == (x, y)
    small_array_2d_complex[x, y] = np.max(small_array_2d_complex) + 1
    assert get_most_salient_point(small_array_2d_complex) == (x, y)
    nb_x, nb_y, nb_z = small_array_3d_float.shape
    x = np.random.randint(nb_x)
    y = np.random.randint(nb_y)
    z = np.random.randint(nb_z)
    small_array_3d_float[x, y, z] = np.max(small_array_3d_float) + 1
    assert get_most_salient_point(small_array_3d_float) == (x, y, z)


def test_find_signal_and_noise(fake_3d_signals_5mhz_float):
    # Get one set of data
    signal = fake_3d_signals_5mhz_float[0, 0]
    # Test it is running, could be better to do a real test by testing few
    # configuration, but since it is very high level and can fail (it expects
    # the user to provide high-level info about noise / signal widths and or
    # locations
    assert find_signal_and_noise(signal)


def test_signal_noise_ratio():
    # Get an example data (wire on water with probes L7-4, PA2 system)
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'pa2_wire.mat'), 'dbsas')
    signal = reader.data[0, 0, 52]
    fs = reader.acquisition_info['sampling_freq']
    signal = us.cpu.filtfilt(signal, 3e6, fs, 'high')
    signal = us.cpu.filtfilt(signal, 8e6, fs, 'low')
    snr = signal_noise_ratio(signal, (2400, 2450), (1000, 2000))
    assert snr == pytest.approx(54.97896933515833)


def test_get_full_width_at_half_maximum():
    # Get an example data (wire on water with probes L7-4, PA2 system)
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'pa2_wire.mat'), 'dbsas')
    x = np.linspace(-20e-3, 20e-3, 500)
    z = np.linspace(5e-3, 50e-3, 1000)
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_setup('sound_speed', 1450)
    fs = reader.acquisition_info['sampling_freq']
    data = us.cpu.filtfilt(reader.data[0], 3e6, fs, 'high')
    data = us.cpu.filtfilt(data, 8e6, fs, 'low')
    beamformed = beamformer.beamform(data, scan)
    envelope = beamformer.compute_envelope(beamformed, scan)
    b_mode = us.cpu.to_b_mode(envelope)
    lateral_peak = 1.2e-3
    axial_peak = 35.1e-3
    lateral_idx = (np.abs(x - lateral_peak)).argmin()
    axial_idx = (np.abs(z - axial_peak)).argmin()
    fwhm = get_full_width_at_half_maximum(b_mode[lateral_idx], axial_idx, z)
    assert fwhm == pytest.approx(0.0003622792247398657)
    fwhm = get_full_width_at_half_maximum(b_mode[:, axial_idx], lateral_idx, x)
    assert fwhm == pytest.approx(0.00047797664481353294)


def test_get_peak_side_lobe():
    # Get an example data (wire on water with probes L7-4, PA2 system)
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'pa2_wire.mat'), 'dbsas')
    x = np.linspace(-20e-3, 20e-3, 500)
    z = np.linspace(5e-3, 50e-3, 1000)
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_setup('sound_speed', 1450)
    fs = reader.acquisition_info['sampling_freq']
    data = us.cpu.filtfilt(reader.data[0], 3e6, fs, 'high')
    data = us.cpu.filtfilt(data, 8e6, fs, 'low')
    beamformed = beamformer.beamform(data, scan)
    envelope = beamformer.compute_envelope(beamformed, scan)
    b_mode = us.cpu.to_b_mode(envelope)
    lateral_peak = 1.2e-3
    axial_peak = 35.1e-3
    lateral_idx = (np.abs(x - lateral_peak)).argmin()
    axial_idx = (np.abs(z - axial_peak)).argmin()
    psl = get_peak_side_lobe(b_mode[lateral_idx], axial_idx, z)
    assert psl == pytest.approx(30.038450419812406)
    psl = get_peak_side_lobe(b_mode[:, axial_idx], lateral_idx, x)
    assert psl == pytest.approx(18.200285564425972)


def test_get_lobe_metrics():
    # Get an example data (wire on water with probes L7-4, PA2 system)
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'pa2_wire.mat'), 'dbsas')
    x = np.linspace(-20e-3, 20e-3, 500)
    z = np.linspace(5e-3, 50e-3, 1000)
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_setup('sound_speed', 1450)
    fs = reader.acquisition_info['sampling_freq']
    data = us.cpu.filtfilt(reader.data[0], 3e6, fs, 'high')
    data = us.cpu.filtfilt(data, 8e6, fs, 'low')
    beamformed = beamformer.beamform(data, scan)
    envelope = beamformer.compute_envelope(beamformed, scan)
    b_mode = us.cpu.to_b_mode(envelope)
    lateral_peak = 1.2e-3
    axial_peak = 35.1e-3
    lateral_idx = (np.abs(x - lateral_peak)).argmin()
    axial_idx = (np.abs(z - axial_peak)).argmin()
    m = get_lobe_metrics(b_mode, (lateral_idx, axial_idx), x, z)
    assert m['axial_fwhm'] == pytest.approx(0.0003622792247398657)
    assert m['lateral_fwhm'] == pytest.approx(0.00047797664481353294)
    assert m['axial_psl'] == pytest.approx(30.038450419812406)
    assert m['lateral_psl'] == pytest.approx(18.200285564425972)


def test_build_mask():
    # The masks builders are tested in the test_mask file directly, but we can
    # test the caller here
    x = np.arange(100)
    z = np.arange(100)
    assert np.any(build_mask((20, 20), 10, x, z, 'circle'))
    assert np.any(build_mask((20, 20), (10, 2), x, z, 'empty_circle'))
    assert np.any(build_mask((20, 20), (10, 20), x, z, 'rectangle'))
    assert np.any(build_mask((20, 20), 10, x, z, 'square'))
    with pytest.raises(AssertionError):
        assert np.any(build_mask((20, 20), 10, x, z, 'empty_circle'))
    with pytest.raises(AssertionError):
        assert np.any(build_mask((20, 20), 10, x, z, 'rectangle'))
    with pytest.raises(AttributeError):
        assert np.any(build_mask((20, 20), 10, x, z, 'wrong_shape'))


def test_get_contrat_noise_ratio():
    # Get an example data (wire on water with probes L7-4, PA2 system)
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'rotating_disk.mat'), 'must')
    x = np.linspace(-12.5, 12.5, 250) * 1e-3
    z = np.linspace(10, 35, 250) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    info = beamformer.setups
    frame = us.cpu.rf2iq(reader.data[0], info['central_freq'],
                         info['sampling_freq'], beamformer.t0)
    beamformed = beamformer.beamform(frame, scan)
    envelope = beamformer.compute_envelope(beamformed, scan)
    b_mode = us.cpu.to_b_mode(envelope)

    signal_mask = build_mask((0,  21.5e-3), 10e-3, x, z, 'circle')
    noise_mask = build_mask((0, 21.5e-3), (14e-3, 2e-3), x, z, 'empty_circle')
    cnr = get_contrat_noise_ratio(b_mode, signal_mask, noise_mask)
    assert cnr == pytest.approx(9.050421335466957)
