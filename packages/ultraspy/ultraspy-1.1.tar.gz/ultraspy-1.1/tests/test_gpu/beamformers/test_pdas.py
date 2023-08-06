"""Unit test file to test our p-DAS beamformer.
"""
import os
import numpy as np

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.pdas import PDelayAndSum
from ultraspy.gpu import gpu_utils
from ultraspy.config import cfg
import ultraspy as us


def test_pdas():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)
    beamformer = PDelayAndSum()
    beamformer_cpu = PDelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    indices = [37]
    data = reader.data[0, indices].copy()
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)

    # Send to GPU
    d_data = gpu_utils.send_to_gpu(data, np.float32)

    # Beamformed
    d_beamformed = beamformer.beamform(d_data, scan)
    beamformed = d_beamformed.get()
    beamformed_cpu = beamformer_cpu.beamform(data, scan)
    tol = np.max(beamformed_cpu) * 1e-3
    assert np.allclose(beamformed, beamformed_cpu, atol=tol)


def test_pdas_iqs():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)
    beamformer = PDelayAndSum(is_iq=True)
    beamformer_cpu = PDelayAndSum(is_iq=True, on_gpu=False)
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
    iqs = us.cpu.rf2iq(data, f0, fs, t0, bandwidth=band)

    # Send to GPU
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)

    # Beamformed
    d_beamformed = beamformer.beamform(d_iqs, scan)
    beamformed = d_beamformed.get()
    beamformed_cpu = beamformer_cpu.beamform(iqs, scan)
    tol = np.max(beamformed_cpu) * 1e-4
    assert np.allclose(beamformed, beamformed_cpu, atol=tol)


def test_pdas_iqs_shen():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z)
    beamformer = PDelayAndSum(is_iq=True, use_shen_version=True)
    beamformer_cpu = PDelayAndSum(is_iq=True, on_gpu=False,
                                  use_shen_version=True)
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
    iqs = us.cpu.rf2iq(data, f0, fs, t0, bandwidth=band)

    # Send to GPU
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)

    # Beamformed
    d_beamformed = beamformer.beamform(d_iqs, scan)
    beamformed = d_beamformed.get()
    beamformed_cpu = beamformer_cpu.beamform(iqs, scan)
    tol = np.max(beamformed_cpu) * 1e-3
    assert np.allclose(beamformed, beamformed_cpu, atol=tol)


def test_pdas_3d():
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    simu_3d = os.path.join(rsc_dir, 'simu_3d_scatterers.mat')
    reader = Reader(simu_3d, 'simu_3d')
    indices = [2]
    data = reader.data[0, indices]
    x = np.linspace(1, 7, 20) * 1e-3
    y = np.linspace(-2, 2, 20) * 1e-3
    z = np.linspace(23, 27, 160) * 1e-3
    scan = GridScan(x, y, z)

    # Beamformers
    beamformer = PDelayAndSum(is_iq=True)
    beamformer_cpu = PDelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer_cpu.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('transmissions_idx', indices)
    beamformer_cpu.update_setup('transmissions_idx', indices)
    beamformer.update_setup('f_number', 1.)
    beamformer_cpu.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'linear')
    beamformer_cpu.update_option('interpolation', 'linear')

    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    d_iqs = gpu_utils.send_to_gpu(iqs, np.complex64)
    d_output = beamformer.beamform(d_iqs, scan)
    output = d_output.get()
    output_cpu = beamformer_cpu.beamform(iqs, scan)
    assert np.allclose(output, output_cpu)


def test_pdas_no_compounding_sum():
    # Data
    rsc_dir = cfg.PATHS_RESOURCES
    picmus = os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5')

    # Beamformers
    beamformer = PDelayAndSum()

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
    d_data = gpu_utils.send_to_gpu(data, np.float32)
    output = beamformer.beamform(d_data, scan).get()

    # Compound all three separately
    beamformer.update_option('compound', True)
    d_data = gpu_utils.send_to_gpu(data[[0]].copy(), np.float32)
    beamformer.update_setup('transmissions_idx', [indices[0]])
    output_tr1 = beamformer.beamform(d_data, scan).get()
    d_data = gpu_utils.send_to_gpu(data[[1]].copy(), np.float32)
    beamformer.update_setup('transmissions_idx', [indices[1]])
    output_tr2 = beamformer.beamform(d_data, scan).get()
    d_data = gpu_utils.send_to_gpu(data[[2]].copy(), np.float32)
    beamformer.update_setup('transmissions_idx', [indices[2]])
    output_tr3 = beamformer.beamform(d_data, scan).get()

    # Compare
    assert np.allclose(output[0], output_tr1)
    assert np.allclose(output[1], output_tr2)
    assert np.allclose(output[2], output_tr3)
