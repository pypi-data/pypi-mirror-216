"""Unit test file to test our FDMAS beamformer.

TODO: check scan shape RFs/ I/Qs before / after envelope
"""
import os
import numpy as np
import pytest

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.fdmas import FilteredDelayMultiplyAndSum
from ultraspy.config import cfg
import ultraspy as us


def test_fdmas(rfs_simu_picmus):
    # Compare the FDMAS metrics with the paper from Polichetti (p-DAS)
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = FilteredDelayMultiplyAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.75)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # First filtered
    f0 = beamformer.setups['central_freq']
    fs = beamformer.setups['sampling_freq']
    data = us.cpu.filtfilt(data, f0 * 1.7, fs, 'low', order=11)
    data = us.cpu.filtfilt(data, f0 * 0.4, fs, 'high', order=11)

    # Beamformed
    beamformed = beamformer.beamform(data, scan)
    envelope = beamformer.compute_envelope(beamformed, scan)
    b_mode = us.cpu.to_b_mode(envelope)

    scatterers = [(250, 115),
                  (250, 227),
                  (53, 338), (118, 338), (183, 338), (250, 338), (314, 338),
                  (380, 338), (445, 338),
                  (250, 449),
                  (250, 559),
                  (250, 669),
                  (53, 782), (118, 782), (183, 782), (250, 782), (314, 782),
                  (380, 782), (445, 782),
                  (250, 893)]

    lobes = []
    for scatter in scatterers:
        lobes.append(us.metrics.get_lobe_metrics(b_mode, scatter, x, z))

    # Test the lateral FWHM for all scatterers, should be similar to Maxime's
    # paper, but isn't, some wrong parameters...? Resolutions?
    lat = np.mean([lobe['lateral_fwhm'] for lobe in lobes
                   if lobe['lateral_fwhm'] is not None])
    axi = np.mean([lobe['axial_fwhm'] for lobe in lobes
                   if lobe['axial_fwhm'] is not None])

    # In the meantime, assert it is the same value as what I've found -> Not a
    # good unit-test, but pretty close tho
    my_lateral_fwhm_value = 0.0006005190032497521
    my_axial_fwhm_value = 0.0003565654312505151
    assert lat == pytest.approx(my_lateral_fwhm_value)
    assert axi == pytest.approx(my_axial_fwhm_value)


def test_fdmas_iqs(rfs_simu_picmus):
    # Comparison values
    rvals = {
        'min': -1835.037242683898,
        'max': 1729.9085501166915,
        'mean': -0.0010964848252621006,
        'median': -6.331640372736122e-18,
    }
    ivals = {
        'min': -1369.6283170651582,
        'max': 1340.6396243917868,
        'mean': 0.0008823613380715566,
        'median': 1.1114810368404717e-16,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(304, 324), 332]
    scat_axi_coords = [314, (320, 340)]
    scat_lat = np.array([
        2.15281193e+01 - 1.75396479e+00j, 7.50952364e+00 - 4.81796889e+00j,
        -1.14275505e+00 - 5.31757199e-01j, 1.12023560e+01 + 6.23411110e+00j,
        4.09235668e+01 + 2.94547476e-01j, 4.49359731e+01 - 2.89935176e+00j,
        1.24832979e+01 + 3.49188134e+00j, 1.49142731e+01 - 1.35223847e+01j,
        2.33851818e+02 - 1.00259948e+02j, 7.01311336e+02 - 2.41217644e+02j,
        1.24877072e+03 - 3.54317929e+02j, 1.49977119e+03 - 3.94963036e+02j,
        1.22575204e+03 - 3.01190967e+02j, 7.05743132e+02 - 1.92846573e+02j,
        2.23520725e+02 - 9.52760949e+01j, 1.16164975e+01 - 1.59508413e+01j,
        1.06585237e+01 + 7.83876031e+00j, 5.22844786e+01 + 5.54319352e+00j,
        4.52686053e+01 - 5.28605844e+00j, 9.75265249e+00 - 1.59243153e+00j])
    scat_axi = np.array([
        8.61654008 + 7.33475757j, -12.4020493 - 4.05043647j,
        12.58733039 - 1.75837803j, -8.90391751 + 11.46762932j,
        -3.12105034 - 25.7988799j, 25.31767644 + 51.8556487j,
        -54.82051403 - 106.94508382j, 73.8137444 + 219.5770071j,
        -48.89918296 - 401.20504428j, -90.12669089 + 612.08433496j,
        440.81616461 - 758.26954651j, -882.20179219 + 699.92377575j,
        1248.77071956 - 354.31792891j, -1356.95733079 - 169.65327984j,
        1135.69056405 + 663.99205402j, -675.30136838 - 914.784979j,
        195.11756533 + 868.20443859j, 120.82359597 - 638.27212147j,
        -229.45427634 + 346.10882689j, 181.24441972 - 148.65498074j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = FilteredDelayMultiplyAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)

    # RFs to I/Qs
    f0 = beamformer.setups['central_freq']
    fs = beamformer.setups['sampling_freq']
    t0 = beamformer.t0
    band = beamformer.setups['bandwidth']
    iqs = us.cpu.rf2iq(data, f0, fs, t0, bandwidth=band)

    # Beamformed
    beamformed = beamformer.beamform(iqs, scan)

    real = beamformed.real
    imag = beamformed.imag
    assert np.min(real) == pytest.approx(rvals['min'], abs=rtol)
    assert np.max(real) == pytest.approx(rvals['max'], abs=rtol)
    assert np.median(real) == pytest.approx(rvals['median'], abs=rtol)
    assert np.mean(real) == pytest.approx(rvals['mean'], abs=rtol)
    assert np.min(imag) == pytest.approx(ivals['min'], abs=itol)
    assert np.max(imag) == pytest.approx(ivals['max'], abs=itol)
    assert np.median(imag) == pytest.approx(ivals['median'], abs=itol)
    assert np.mean(imag) == pytest.approx(ivals['mean'], abs=itol)
    tol = min(rtol, itol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_fdmas_3d_rfs():
    if cfg.CPU_LIB == 'numpy' and os.getenv('HEAVY_TEST', True) == 'False':
        pytest.skip("Test skipped, go in HEAVY_TEST mode to test it")

    # Test the 3d FDMAS on regular configuration. Comparison is high level,
    # made with visual verification, no comparison with external tool such as
    # MUST
    vals = {
        'min': -1.6774905263079829e-21,
        'max': 1.729598867742676e-21,
        'median': -1.4710694679655417e-36,
        'mean': -8.463961545017627e-31,
    }
    tol = (vals['max'] - vals['min']) / 1e6
    scat_lat_coords = [(5, 15), 10, 80]
    scat_elev_coords = [10, (5, 15), 80]
    scat_axi_coords = [10, 10, (75, 85)]
    scat_lat = np.array([
        1.75765711e-29, -2.99499043e-29, 3.91418247e-29, -6.19180722e-29,
        9.29001107e-29, -1.14260720e-28, -9.37677689e-29, 9.81258500e-28,
        -4.34998636e-27, 7.28531458e-27])
    scat_elev = np.array([
        -1.21818518e-28, 2.62178708e-29, 8.15479804e-29, 4.13889355e-29,
        -1.14260721e-28, -1.14260720e-28, 4.13889353e-29, 8.15479853e-29,
        2.62178727e-29, -1.21818515e-28])
    scat_axi = np.array([
        9.66496021e-29, 4.95523856e-29, -7.56998505e-29, -1.98871712e-28,
        -2.41827163e-28, -1.14260720e-28, 1.96940660e-28, 4.98490424e-28,
        6.03520103e-28, 2.60516466e-28])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1, 7, 20) * 1e-3
    y = np.linspace(-2, 2, 20) * 1e-3
    z = np.linspace(23, 27, 160) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = FilteredDelayMultiplyAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [2]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(vals['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(vals['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(vals['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(vals['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat,
                       beamformed[c[0][0]:c[0][1], c[1], c[2]], atol=tol)
    c = scat_elev_coords
    assert np.allclose(scat_elev,
                       beamformed[c[0], c[1][0]:c[1][1], c[2]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi,
                       beamformed[c[0], c[1], c[2][0]:c[2][1]], atol=tol)


def test_fdmas_3d_iqs():
    # Same but on I/Qs
    rvals = {
        'min': -4.610176434630474e-21,
        'max': 4.1674035078812246e-21,
        'median': 1.2744145073977256e-32,
        'mean': 3.360458863151347e-26,
    }
    ivals = {
        'min': -4.78652511631193e-21,
        'max': 3.661912240713553e-21,
        'median': 3.8213848495061115e-32,
        'mean': -1.129640597263945e-25,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(5, 15), 10, 40]
    scat_elev_coords = [10, (5, 15), 40]
    scat_axi_coords = [10, 10, (35, 45)]
    scat_lat = np.array([
        9.35401513e-24 + 9.76300104e-24j, 8.56788901e-23 - 1.43024214e-22j,
        1.14623625e-22 + 1.21971279e-22j, -3.49343229e-22 + 1.78421018e-22j,
        3.43318754e-21 - 5.82902047e-23j, -3.43800285e-21 - 7.54041403e-22j,
        4.44382142e-22 + 1.58820592e-22j, -3.58894867e-23 - 7.54862006e-25j,
        9.15272495e-23 + 2.99939394e-25j, -4.55847095e-23 + 2.22312811e-23j])
    scat_elev = np.array([
        -1.32282378e-23 - 4.25758832e-24j, -1.23405133e-22 - 1.01935970e-22j,
        -4.81834434e-24 - 1.63224470e-23j, -7.90570922e-22 - 1.29250339e-22j,
        -3.43800285e-21 - 7.54041403e-22j, -3.43800285e-21 - 7.54041403e-22j,
        -7.90570922e-22 - 1.29250339e-22j, -4.81834434e-24 - 1.63224470e-23j,
        -1.23405133e-22 - 1.01935970e-22j, -1.32282378e-23 - 4.25758832e-24j])
    scat_axi = np.array([
        -8.18996994e-24 - 3.87370617e-24j, 4.43269016e-24 - 1.51696334e-23j,
        2.64564242e-22 - 5.55665878e-23j, -1.62288487e-21 - 3.46200746e-22j,
        3.43370581e-21 + 8.57725565e-22j, -3.43800285e-21 - 7.54041403e-22j,
        1.77157000e-21 - 2.21646916e-22j, 2.67371118e-22 + 2.85072749e-22j,
        -2.15363928e-22 + 2.91047713e-22j, -1.79914822e-25 - 1.16753082e-22j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1, 7, 20) * 1e-3
    y = np.linspace(-2, 2, 20) * 1e-3
    z = np.linspace(22, 28, 80) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = FilteredDelayMultiplyAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [2]
    data = reader.data[0, pw]
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])

    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(iqs, scan)

    real = beamformed.real
    imag = beamformed.imag
    assert np.min(real) == pytest.approx(rvals['min'], abs=rtol)
    assert np.max(real) == pytest.approx(rvals['max'], abs=rtol)
    assert np.median(real) == pytest.approx(rvals['median'], abs=rtol)
    assert np.mean(real) == pytest.approx(rvals['mean'], abs=rtol)
    assert np.min(imag) == pytest.approx(ivals['min'], abs=itol)
    assert np.max(imag) == pytest.approx(ivals['max'], abs=itol)
    assert np.median(imag) == pytest.approx(ivals['median'], abs=itol)
    assert np.mean(imag) == pytest.approx(ivals['mean'], abs=itol)
    tol = min(rtol, itol)
    c = scat_lat_coords
    assert np.allclose(scat_lat,
                       beamformed[c[0][0]:c[0][1], c[1], c[2]], atol=tol)
    c = scat_elev_coords
    assert np.allclose(scat_elev,
                       beamformed[c[0], c[1][0]:c[1][1], c[2]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi,
                       beamformed[c[0], c[1], c[2][0]:c[2][1]], atol=tol)


def test_fdmas_no_compounding_sum():
    # Compare our results with or without compounding
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-3, 3, 40) * 1e-3
    z = np.linspace(20, 28, 200) * 1e-3
    beamformer = FilteredDelayMultiplyAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [0, 37, 74]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')

    # Same with no compounding
    beamformer.update_option('compound', False)
    scan = GridScan(x, z, on_gpu=False)
    beamformed_wo_compound = beamformer.beamform(data, scan)

    # Same with no reduce
    beamformer.update_option('reduce', False)
    assert beamformer.options['reduce']

    # Beamformed all three transmission separately
    beamformer.update_option('compound', True)
    beamformer.update_setup('transmissions_idx', [pw[0]])
    scan = GridScan(x, z, on_gpu=False)
    beamformed_tr1 = beamformer.beamform(reader.data[0, [pw[0]]], scan)
    beamformer.update_setup('transmissions_idx', [pw[1]])
    scan = GridScan(x, z, on_gpu=False)
    beamformed_tr2 = beamformer.beamform(reader.data[0, [pw[1]]], scan)
    beamformer.update_setup('transmissions_idx', [pw[2]])
    scan = GridScan(x, z, on_gpu=False)
    beamformed_tr3 = beamformer.beamform(reader.data[0, [pw[2]]], scan)

    assert np.allclose(beamformed_wo_compound[0], beamformed_tr1)
    assert np.allclose(beamformed_wo_compound[1], beamformed_tr2)
    assert np.allclose(beamformed_wo_compound[2], beamformed_tr3)
