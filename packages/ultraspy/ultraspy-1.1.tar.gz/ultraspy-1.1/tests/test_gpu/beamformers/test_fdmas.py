"""Unit test file to test our FDMAS beamformer.
"""
import os
import numpy as np

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.fdmas import FilteredDelayMultiplyAndSum
from ultraspy.gpu import gpu_utils
from ultraspy.config import cfg
import ultraspy as us


def test_envelope_gpu_equals_cpu():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-10, 10, 100) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    beamformer = FilteredDelayMultiplyAndSum()
    beamformer_cpu = FilteredDelayMultiplyAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    indices = [37]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)

    # Send to GPU
    d_data = gpu_utils.send_to_gpu(data, np.float32)

    # Beamformed
    scan = GridScan(x, z)
    d_beamformed = beamformer.beamform(d_data, scan)
    d_envelope = beamformer.compute_envelope(d_beamformed, scan)
    output = d_envelope.get()
    beamformed_cpu = beamformer_cpu.beamform(data, scan)
    output_cpu = beamformer_cpu.compute_envelope(beamformed_cpu, scan)
    tol = np.max(beamformed_cpu) * 1e-3
    assert np.allclose(output, output_cpu, atol=tol)


def test_fdmas_gpu_equals_cpu():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-10, 10, 100) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    beamformer = FilteredDelayMultiplyAndSum()
    beamformer_cpu = FilteredDelayMultiplyAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    indices = [37]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)

    # Send to GPU
    d_data = gpu_utils.send_to_gpu(data, np.float32)

    # Beamformed
    scan = GridScan(x, z)
    d_beamformed = beamformer.beamform(d_data, scan)
    beamformed = d_beamformed.get()
    scan = GridScan(x, z)
    beamformed_cpu = beamformer_cpu.beamform(data, scan)
    tol = np.max(beamformed_cpu) * 1e-3
    assert np.allclose(beamformed, beamformed_cpu, atol=tol)


def test_fdmas_iterate_rfs():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    beamformer = FilteredDelayMultiplyAndSum()
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    indices = [37]
    data = reader.data[0, indices]
    beamformer.update_setup('transmissions_idx', indices)

    # Send to GPU
    d_data = gpu_utils.send_to_gpu(data, np.float32)

    # Beamformed
    for _ in range(10):
        scan = GridScan(x, z)
        beamformer.beamform(d_data, scan).get()


def test_fdmas_iqs_gpu_equals_cpu():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-10, 10, 100) * 1e-3
    z = np.linspace(30, 40, 200) * 1e-3
    beamformer = FilteredDelayMultiplyAndSum(is_iq=True)
    beamformer_cpu = FilteredDelayMultiplyAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    indices = [37]
    data = reader.data[0, indices]
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)

    # RFs to I/Qs
    f0 = beamformer.setups['central_freq']
    fs = beamformer.setups['sampling_freq']
    t0 = beamformer.t0
    band = beamformer.setups['bandwidth']
    iqs = us.cpu.rf2iq(data, f0, fs, t0, bandwidth=band).copy()

    # Send to GPU
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)

    # Beamformed
    scan = GridScan(x, z)
    d_beamformed = beamformer.beamform(d_iqs, scan)
    beamformed = d_beamformed.get()
    scan = GridScan(x, z)
    beamformed_cpu = beamformer_cpu.beamform(iqs, scan)

    # Compare
    tol = np.abs(np.max(beamformed_cpu)) * 1e-4
    assert np.allclose(beamformed, beamformed_cpu, atol=tol)


def test_fdmas_3d():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    simu_3d = os.path.join(rsc_dir, 'simu_3d_scatterers.mat')
    reader = Reader(simu_3d, 'simu_3d')
    indices = [2]
    data = reader.data[0, indices]
    x = np.linspace(1, 7, 20) * 1e-3
    y = np.linspace(-2, 2, 20) * 1e-3
    z = np.linspace(22, 28, 80) * 1e-3

    # Beamformers
    beamformer = FilteredDelayMultiplyAndSum(is_iq=True)
    beamformer_cpu = FilteredDelayMultiplyAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)

    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)
    scan = GridScan(x, y, z)
    d_output = beamformer.beamform(d_iqs, scan)
    output = d_output.get()
    scan = GridScan(x, y, z)
    output_cpu = beamformer_cpu.beamform(iqs, scan)
    assert np.allclose(output, output_cpu)


def test_fdmas_no_compounding_sum():
    # Data
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')

    # Beamformers
    beamformer = FilteredDelayMultiplyAndSum()

    # Picmus
    reader = Reader(picmus, 'picmus')
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3

    # Compounding with three random angles
    indices = [0, 5, 70]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer.update_option('compound', False)
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    scan = GridScan(x, z)
    output = beamformer.beamform(d_data, scan).get()

    # Compound all three separately
    beamformer.update_option('compound', True)
    d_data = gpu_utils.send_to_gpu(data[[0]].copy(), np.float32)
    beamformer.update_setup('transmissions_idx', [indices[0]])
    scan = GridScan(x, z)
    output_tr1 = beamformer.beamform(d_data, scan).get()
    d_data = gpu_utils.send_to_gpu(data[[1]].copy(), np.float32)
    beamformer.update_setup('transmissions_idx', [indices[1]])
    scan = GridScan(x, z)
    output_tr2 = beamformer.beamform(d_data, scan).get()
    d_data = gpu_utils.send_to_gpu(data[[2]].copy(), np.float32)
    beamformer.update_setup('transmissions_idx', [indices[2]])
    scan = GridScan(x, z)
    output_tr3 = beamformer.beamform(d_data, scan).get()

    # Compare
    assert np.allclose(output[0], output_tr1)
    assert np.allclose(output[1], output_tr2)
    assert np.allclose(output[2], output_tr3)
