"""Unit test file to test our p-DAS beamformer.
"""
import os
import numpy as np
import pytest

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.pdas import PDelayAndSum
from ultraspy.config import cfg
import ultraspy as us


def test_pdas(rfs_simu_picmus):
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = PDelayAndSum(on_gpu=False)
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
    my_lateral_fwhm_value = 0.0005448144524200453
    my_axial_fwhm_value = 0.0003938227362281762
    assert lat == pytest.approx(my_lateral_fwhm_value)
    assert axi == pytest.approx(my_axial_fwhm_value)


def test_pdas_iqs(rfs_simu_picmus):
    # Comparison values
    rvals = {
        'min': -1772.4460766261307,
        'max': 1727.9077764463184,
        'mean': 0.003734305005148506,
        'median': 1.0628561248659883e-11,
    }
    ivals = {
        'min': -1852.7702761485739,
        'max': 1560.2708987086767,
        'mean': 0.012093869588195128,
        'median': 2.173256866368058e-12,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(304, 324), 332]
    scat_axi_coords = [314, (320, 340)]
    scat_lat = np.array([
        -2.15816113e+01 + 8.77707354e-01j, -8.56175480e+00 + 2.51040322e+00j,
        -2.72309754e-01 + 1.23065113e+00j, 1.24091318e+01 + 3.22030603e+00j,
        4.09243618e+01 + 1.47274692e-01j, 4.50060460e+01 - 1.45042851e+00j,
        1.28421279e+01 + 1.76230343e+00j, -1.87821988e+01 + 7.24702956e+00j,
        -2.49238374e+02 + 5.11758021e+01j, -7.31485160e+02 + 1.22282468e+02j,
        -1.28568144e+03 + 1.78865171e+02j, -1.53806917e+03 + 1.99129712e+02j,
        -1.25306531e+03 + 1.51694981e+02j, -7.25119547e+02 + 9.72872657e+01j,
        -2.38065125e+02 + 4.86214435e+01j, -1.75868577e+01 + 8.94845186e+00j,
        1.25711885e+01 + 4.12498588e+00j, 5.25041949e+01 + 2.77546649e+00j,
        4.54992283e+01 - 2.64749985e+00j, 9.84946390e+00 - 7.98830166e-01j])
    scat_axi = np.array([
        -10.61943952 - 3.90780446e+00j, 2.05070926 - 1.28845432e+01j,
        12.67896177 - 8.81310396e-01j, 6.3841569 + 1.30395096e+01j,
        -17.23682808 + 1.94477484e+01j, -48.94372894 - 3.05696653e+01j,
        62.66724952 - 1.02544408e+02j, 188.09786495 + 1.35209926e+02j,
        -267.94853942 + 3.02589157e+02j, -404.35757697 - 4.68257412e+02j,
        760.23951295 - 4.37409967e+02j, 370.60600402 + 1.06340232e+03j,
        -1285.68143617 + 1.78865171e+02j, 84.99094065 - 1.36487801e+03j,
        1269.79114812 + 3.43960674e+02j, -512.35621324 + 1.01506384e+03j,
        -694.79386067 - 5.55977790e+02j, 500.23870911 - 4.14428373e+02j,
        196.41471466 + 3.65871350e+02j, -220.71844973 + 7.89380068e+01j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = PDelayAndSum(is_iq=True, on_gpu=False)
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


def test_pdas_iqs_shen(rfs_simu_picmus):
    # Comparison values
    rvals = {
        'min': -1835.037242683898,
        'max': 1729.9085501166915,
        'mean': -0.0010964848252620998,
        'median': -6.331640372736122e-18,
    }
    ivals = {
        'min': -1369.6283170651582,
        'max': 1340.6396243917868,
        'mean': 0.0008823613380715558,
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
    beamformer = PDelayAndSum(is_iq=True, use_shen_version=True, on_gpu=False)
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


def test_pdas_3d_rfs():
    # Test the 3d p-DAS on regular configuration. Comparison is high level,
    # made with visual verification, no comparison with external tool such as
    # MUST
    vals = {
        'min': -5.98869862479345e-21,
        'max': 5.259296696381273e-21,
        'median': 6.346384164679553e-32,
        'mean': 4.14918909499915e-30,
    }
    tol = (vals['max'] - vals['min']) / 1e6
    scat_lat_coords = [(5, 15), 10, 80]
    scat_elev_coords = [10, (5, 15), 80]
    scat_axi_coords = [10, 10, (75, 85)]
    scat_lat = np.array([
        2.51477553e-24, -4.23272783e-23, 1.83957903e-23, -3.69065416e-22,
        1.98571952e-23, 3.99894178e-21, -8.70926220e-24, 3.78931606e-23,
        -5.19567063e-24, 7.49563079e-23])
    scat_elev = np.array([
        -2.04913022e-23, -1.66527999e-22, -6.97809488e-24, 9.71952168e-22,
        3.99894178e-21, 3.99894178e-21, 9.71952168e-22, -6.97809488e-24,
        -1.66527999e-22, -2.04913022e-23])
    scat_axi = np.array([
        7.15807407e-23, 2.55533137e-21, -8.74239270e-23, -3.81666115e-21,
        9.79746489e-23, 3.99894178e-21, -2.90375098e-23, -2.97497979e-21,
        -1.33820099e-22, 1.42935731e-21])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1, 7, 20) * 1e-3
    y = np.linspace(-2, 2, 20) * 1e-3
    z = np.linspace(23, 27, 160) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = PDelayAndSum(on_gpu=False)
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


def test_pdas_3d_iqs():
    # Same but on I/Qs
    rvals = {
        'min': -6.181325772370182e-21,
        'max': 5.613418766992339e-21,
        'median': -2.075956584116581e-28,
        'mean': -3.2000339735610898e-25,
    }
    ivals = {
        'min': -5.8913260207124164e-21,
        'max': 6.07917714213734e-21,
        'median': 4.780346730224878e-28,
        'mean': 7.848389338794763e-26,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(5, 15), 10, 80]
    scat_elev_coords = [10, (5, 15), 80]
    scat_axi_coords = [10, 10, (75, 85)]
    scat_lat = np.array([
        2.19216144e-25 - 1.18522757e-24j, -4.83805779e-23 - 2.07389206e-22j,
        7.52041734e-23 - 1.39873685e-22j, -3.49661900e-22 + 6.96946903e-23j,
        1.28992658e-23 - 3.64781529e-21j, 3.72705043e-21 + 4.27809084e-22j,
        -9.94574488e-23 + 3.98487251e-22j, 6.60994119e-23 + 9.26806899e-24j,
        -1.52081554e-23 + 6.89478079e-23j, 5.89213663e-23 - 1.13171569e-23j])
    scat_elev = np.array([
        -7.29085731e-24 - 4.71684148e-24j, -1.59161216e-22 - 6.98858240e-23j,
        -1.91603663e-23 - 8.32531222e-24j, 8.23804491e-22 + 1.00745153e-22j,
        3.72705043e-21 + 4.27809084e-22j, 3.72705043e-21 + 4.27809084e-22j,
        8.23804491e-22 + 1.00745153e-22j, -1.91603663e-23 - 8.32531222e-24j,
        -1.59161216e-22 - 6.98858240e-23j, -7.29085731e-24 - 4.71684148e-24j])
    scat_axi = np.array([
        2.51095071e-22 - 1.66048557e-21j, 2.41552594e-21 + 3.65463056e-22j,
        -4.47705085e-22 + 3.07057801e-21j, -3.50906337e-21 - 4.84563693e-22j,
        4.78168090e-22 - 3.73355827e-21j, 3.72705043e-21 + 4.27809084e-22j,
        -3.28168848e-22 + 3.50763187e-21j, -3.07650521e-21 - 1.84878472e-22j,
        5.56343335e-24 - 2.47927254e-21j, 1.79509434e-21 - 1.85450122e-22j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1, 7, 20) * 1e-3
    y = np.linspace(-2, 2, 20) * 1e-3
    z = np.linspace(23, 27, 160) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = PDelayAndSum(is_iq=True, on_gpu=False)
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


def test_pdas_no_compounding_sum():
    # Compare our results with or without compounding
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-19.05, 19.05, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = PDelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [0, 37, 74]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')

    # Same with no compounding
    beamformer.update_option('compound', False)
    beamformed_wo_compound = beamformer.beamform(data, scan)

    # Same with no reduce
    beamformer.update_option('reduce', False)
    assert beamformer.options['reduce']

    # Beamformed all three transmission separately
    beamformer.update_option('compound', True)
    beamformer.update_setup('transmissions_idx', [pw[0]])
    beamformed_tr1 = beamformer.beamform(reader.data[0, [pw[0]]], scan)
    beamformer.update_setup('transmissions_idx', [pw[1]])
    beamformed_tr2 = beamformer.beamform(reader.data[0, [pw[1]]], scan)
    beamformer.update_setup('transmissions_idx', [pw[2]])
    beamformed_tr3 = beamformer.beamform(reader.data[0, [pw[2]]], scan)

    assert np.allclose(beamformed_wo_compound[0], beamformed_tr1)
    assert np.allclose(beamformed_wo_compound[1], beamformed_tr2)
    assert np.allclose(beamformed_wo_compound[2], beamformed_tr3)
