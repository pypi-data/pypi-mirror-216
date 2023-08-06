"""Unit test file to test our DAS beamformer.
"""
import os
import numpy as np

from ultraspy.gpu import gpu_utils
from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.das import DelayAndSum
from ultraspy.config import cfg
import ultraspy as us


def difference_is_below(output1, output2, percentage=0.1, rel_tol=1e-1,
                        abs_tol=1e-6):
    tol = min(np.max(output1) - np.min(output1),
              np.max(output2) - np.min(output2))
    perc = np.mean(np.abs(output1 - output2) < tol * abs_tol)
    if 1 - perc < percentage:
        return np.allclose(output1, output2, atol=tol*rel_tol)
    return False


def test_das_equals_must():
    # Test with some high-level values from MUST
    must_vals = {
        '75pw': 1.112148107577985e+03,
        'low_res': 15.718527181427977,
        'high_res': 15.319718573702600,
        'fnb6': 5.224738956470701,
        'iqs': 19.096481361837270,
    }

    # File
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    reader = Reader(picmus, 'picmus')
    data = reader.data[0].copy()
    d_data = gpu_utils.send_to_gpu(data, np.float32)

    # Beamformers
    beamformer = DelayAndSum()
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.75)
    beamformer.update_setup('signal_duration', 0)

    # Scans
    x = np.linspace(-20, 20, 101) * 1e-3
    z = np.linspace(5, 50, 200) * 1e-3
    small_scan = GridScan(x, z)
    x = np.linspace(-20, 20, 801) * 1e-3
    z = np.linspace(5, 50, 1600) * 1e-3
    big_scan = GridScan(x, z)

    # 75 PW
    output = beamformer.beamform(d_data, small_scan).get().T
    actual_max = np.max(np.abs(output[50:150, 25:75]))
    assert 0.999 < (must_vals['75pw'] / actual_max) < 1.001
    assert np.max(np.abs(output - output[:, ::-1])) < np.ptp(output) * 1e-6

    # Convert to 1 transmission
    data = data[[37]].copy()
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    beamformer.update_setup('transmissions_idx', [37])

    # Low res
    output = beamformer.beamform(d_data, small_scan).get().T
    actual_max = np.max(np.abs(output[50:150, 25:75]))
    assert 0.999 < (must_vals['low_res'] / actual_max) < 1.001
    assert np.max(np.abs(output - output[:, ::-1])) < np.ptp(output) * 1e-6

    # High resolution
    output = beamformer.beamform(d_data, big_scan).get().T
    actual_max = np.max(np.abs(output[400:1200, 200:600]))
    assert 0.999 < (must_vals['high_res'] / actual_max) < 1.001
    assert np.max(np.abs(output - output[:, ::-1])) < np.ptp(output) * 1e-6

    # f-number = 6 (ridiculous value, but proof of concept)
    beamformer.update_setup('f_number', 6.)
    output = beamformer.beamform(d_data, small_scan).get().T
    actual_max = np.max(np.abs(output[50:150, 25:75]))
    assert 0.999 < (must_vals['fnb6'] / actual_max) < 1.001
    assert np.max(np.abs(output - output[:, ::-1])) < np.ptp(output) * 1e-6

    # I/Qs
    beamformer.update_setup('f_number', 1.75)
    beamformer.set_is_iq(True)
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=200)
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)
    output = beamformer.beamform(d_iqs, small_scan).get().T
    actual_max = np.max(np.abs(output[50:150, 25:75]))
    assert 0.999 < (must_vals['iqs'] / actual_max) < 1.001
    assert np.max(np.abs(output - output[:, ::-1])) < np.ptp(output) * 1e-6


def test_das_cpu_equals_gpu():
    # Data
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    sta_pa2 = os.path.join(rsc_dir, 'pa2_sta.mat')
    convex_simu = os.path.join(rsc_dir, 'simu_convex_scatterers.mat')
    simu_3d = os.path.join(rsc_dir, 'simu_3d_scatterers.mat')

    # Beamformers
    beamformer = DelayAndSum()
    beamformer_cpu = DelayAndSum(on_gpu=False)

    # STA
    reader = Reader(sta_pa2, 'dbsas')
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('sound_speed', 1440)
    beamformer_cpu.update_setup('sound_speed', 1440)
    indices = list(range(64, 96, 3))
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)
    x = np.linspace(0, 10, 50) * 1e-3
    z = np.linspace(40, 50, 400) * 1e-3
    scan = GridScan(x, z)
    d_output = beamformer.beamform(data, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert difference_is_below(output, output_cpu)

    # Picmus
    reader = Reader(picmus, 'picmus')
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)

    # Compounding with three random angles
    indices = [0, 5, 70]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)
    output = beamformer.beamform(data, scan).get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert difference_is_below(output, output_cpu)

    # Central data
    indices = [37]
    data = reader.data[0, indices]
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)
    d_output = beamformer.beamform(data, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert difference_is_below(output, output_cpu)

    # Test no interpolation
    beamformer.update_option('interpolation', 'none')
    beamformer_cpu.update_option('interpolation', 'none')
    d_output = beamformer.beamform(data, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert difference_is_below(output, output_cpu)

    # Test mean (DAM instead of DAS)
    beamformer.update_option('reduction', 'mean')
    beamformer_cpu.update_option('reduction', 'mean')
    d_output = beamformer.beamform(data, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert difference_is_below(output, output_cpu)

    # Test apodization
    if cfg.CPU_LIB != 'numpy':
        beamformer.update_option('rx_apodization', 'tukey')
        beamformer_cpu.update_option('rx_apodization', 'tukey')
        d_output = beamformer.beamform(data, scan)
        output = d_output.get()
        output_cpu = beamformer_cpu.beamform(data, scan)
        assert difference_is_below(output, output_cpu)

    # Test Convex
    reader = Reader(convex_simu, 'simus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    data = reader.data[0].copy()
    d_output = beamformer.beamform(data, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    output_cpu = np.nan_to_num(output_cpu, nan=0)
    assert difference_is_below(output, output_cpu, abs_tol=1e-5)

    # Test 3D
    reader = Reader(simu_3d, 'simu_3d')
    data = reader.data[0]
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    d_output = beamformer.beamform(data, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert np.allclose(output, output_cpu)


def test_iqs():
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')
    reader = Reader(picmus, 'picmus')
    x = np.linspace(-20, 20, 200) * 1e-3
    z = np.linspace(5, 50, 500) * 1e-3
    scan = GridScan(x, z)

    # Beamformers
    beamformer = DelayAndSum(is_iq=True)
    beamformer_cpu = DelayAndSum(on_gpu=False, is_iq=True)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    indices = [0, 37, 74]
    data = reader.data[0, indices]
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)

    # Test on I/Qs
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0)

    # Beamform
    beamformed = beamformer.beamform(iqs, scan).get()
    beamformed_cpu = beamformer_cpu.beamform(iqs, scan)

    assert difference_is_below(beamformed, beamformed_cpu)


def test_3d_iqs():
    rsc_dir = cfg.PATHS_RESOURCES
    file = os.path.join(rsc_dir, 'simu_3d_scatterers.mat')
    reader = Reader(file, 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z)

    # Beamformers
    beamformer = DelayAndSum(is_iq=True)
    beamformer_cpu = DelayAndSum(on_gpu=False, is_iq=True)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)

    # Test a few frames on I/Qs
    info = beamformer.setups
    iqs = us.cpu.rf2iq(reader.data[0], info['central_freq'],
                       info['sampling_freq'], beamformer.t0)

    # Beamform
    beamformed = beamformer.beamform(iqs, scan).get()
    beamformed_cpu = beamformer_cpu.beamform(iqs, scan)

    assert difference_is_below(beamformed, beamformed_cpu)


def test_packet_data():
    # Makes sure the beamform packet works as the frame by frame version
    rsc_dir = cfg.PATHS_RESOURCES
    disk = os.path.join(rsc_dir, 'rotating_disk.mat')

    # Beamformers
    beamformer = DelayAndSum(is_iq=True)
    beamformer_cpu = DelayAndSum(is_iq=True, on_gpu=False)

    # Reader, 5 frames enough for testing
    reader = Reader(disk, 'must')
    data = reader.data[:5, :]
    data = us.cpu.rf2iq(data, reader.probe.central_freq,
                        reader.acquisition_info['sampling_freq'], 0)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_option('interpolation', 'linear')
    beamformer_cpu.update_option('interpolation', 'linear')
    x = np.linspace(-12.5, 12.5, 250) * 1e-3
    z = np.linspace(10, 35, 250) * 1e-3
    scan = GridScan(x, z, on_gpu=False)

    # Beamform everything
    output = beamformer.beamform_packet(data, scan).get()
    output_cpu = beamformer_cpu.beamform_packet(data, scan)
    assert output.shape == output_cpu.shape
    assert difference_is_below(output, output_cpu, abs_tol=1e-5)


def test_das_no_compounding():
    # Data
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')

    # Beamformers
    beamformer = DelayAndSum()
    beamformer_cpu = DelayAndSum(on_gpu=False)

    # Picmus
    reader = Reader(picmus, 'picmus')
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)

    # Compounding with three random angles
    indices = [0, 5, 70]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)
    beamformer.update_option('compound', False)
    beamformer_cpu.update_option('compound', False)
    output = beamformer.beamform(data, scan).get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert output_cpu.ndim == 3
    assert output_cpu.shape[0] == len(indices)
    assert output.shape == output_cpu.shape
    assert difference_is_below(output, output_cpu)

    # No reduce
    beamformer.update_option('reduce', False)
    beamformer_cpu.update_option('reduce', False)
    output = beamformer.beamform(data, scan).get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert output_cpu.ndim == 4
    assert output_cpu.shape[0] == len(indices)
    assert output_cpu.shape[1] == reader.probe.nb_elements
    assert output.shape == output_cpu.shape
    assert difference_is_below(output, output_cpu, abs_tol=1e-5)

    # No reduce but compounding
    beamformer.update_option('compound', True)
    beamformer_cpu.update_option('compound', True)
    output = beamformer.beamform(data, scan).get()
    output_cpu = beamformer_cpu.beamform(data, scan)
    assert output_cpu.ndim == 3
    assert output_cpu.shape[0] == reader.probe.nb_elements
    assert output.shape == output_cpu.shape
    assert difference_is_below(output, output_cpu, abs_tol=1e-5)


def test_das_no_compounding_sum():
    # Data
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')

    # Beamformers
    beamformer = DelayAndSum()

    # Picmus
    reader = Reader(picmus, 'picmus')
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)

    # Compounding with three random angles
    indices = [0, 5, 70]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer.update_option('compound', False)
    output = beamformer.beamform(data, scan).get()

    # Compound all three separately
    beamformer.update_option('compound', True)
    beamformer.update_setup('transmissions_idx', [indices[0]])
    output_tr1 = beamformer.beamform(data[[0]], scan).get()
    beamformer.update_setup('transmissions_idx', [indices[1]])
    output_tr2 = beamformer.beamform(data[[1]], scan).get()
    beamformer.update_setup('transmissions_idx', [indices[2]])
    output_tr3 = beamformer.beamform(data[[2]], scan).get()

    # Compare
    assert np.allclose(output[0], output_tr1)
    assert np.allclose(output[1], output_tr2)
    assert np.allclose(output[2], output_tr3)


def test_das_no_compounding_mean():
    # Data
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')

    # Beamformers
    beamformer = DelayAndSum()

    # Picmus
    reader = Reader(picmus, 'picmus')
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)

    # Compounding with three random angles
    indices = [0, 5, 70]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer.update_option('compound', False)
    beamformer.update_option('reduction', 'mean')
    output = beamformer.beamform(data, scan).get()

    # Compound all three separately
    beamformer.update_option('compound', True)
    beamformer.update_setup('transmissions_idx', [indices[0]])
    output_tr1 = beamformer.beamform(data[[0]], scan).get()
    beamformer.update_setup('transmissions_idx', [indices[1]])
    output_tr2 = beamformer.beamform(data[[1]], scan).get()
    beamformer.update_setup('transmissions_idx', [indices[2]])
    output_tr3 = beamformer.beamform(data[[2]], scan).get()

    # Compare
    assert np.allclose(output[0], output_tr1)
    assert np.allclose(output[1], output_tr2)
    assert np.allclose(output[2], output_tr3)
