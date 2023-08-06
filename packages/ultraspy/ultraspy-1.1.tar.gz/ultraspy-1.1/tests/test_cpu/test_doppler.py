"""Unit test file for testing the Doppler methods.
"""
import os
import numpy as np
import scipy.signal
import scipy.ndimage
import pytest

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan
from ultraspy.beamformers.das import DelayAndSum
from ultraspy.config import cfg
import ultraspy as us

from ultraspy.cpu import (apply_wall_filter,
                          spatial_smoothing,
                          get_color_doppler_map,
                          get_power_doppler_map)


def test_mean_wall_filter(fake_3d_signals_5mhz_complex):
    # The mean wall filter is pretty basic, so we just trivially test if its
    # regular mode still works as it should
    filtered = apply_wall_filter(fake_3d_signals_5mhz_complex, 'mean', axis=0)
    means = np.mean(fake_3d_signals_5mhz_complex, axis=0)[None, ...]
    assert np.allclose(filtered, fake_3d_signals_5mhz_complex - means)


def test_poly_wall_filter(fake_3d_signals_5mhz_complex):
    # This should test the validity of the wall filter itself... Should be done
    # on real data, we can actually do polynomial regression and check if the
    # first degrees has been lowered to close to zero.
    filtered = apply_wall_filter(fake_3d_signals_5mhz_complex, 'poly', axis=0)
    assert filtered is not None


def test_poly_wall_filter_shapes(fake_3d_signals_5mhz_complex):
    # Ensure the polynomial regression works on different shapes, and that we
    # have the same results when transposed data
    degree = 3

    # Test the transposed format (nb_f, nb_p), which is not flexible to a
    # flexible number of dimensions (doesn't aim to be the main version)
    iqs1 = fake_3d_signals_5mhz_complex.copy()
    nb_x, nb_z, nb_f = iqs1.shape
    iqs1 = iqs1.transpose((2, 0, 1)).reshape(nb_f, -1)
    f_iqs1 = apply_wall_filter(iqs1, 'poly', degree, axis=0)
    f_iqs1 = f_iqs1.reshape(nb_f, nb_x, nb_z).transpose((1, 2, 0))

    # Test the regular flattened format (nb_p, nb_f)
    iqs2 = fake_3d_signals_5mhz_complex.copy()
    nb_x, nb_z, nb_f = iqs2.shape
    iqs2 = iqs2.reshape(-1, nb_f)
    f_iqs2 = apply_wall_filter(iqs2, 'poly', degree, axis=-1)
    f_iqs2 = f_iqs2.reshape(nb_x, nb_z, nb_f)

    # Test the regular format (..., nb_f), not flattened, flexible to any
    # dimension
    iqs3 = fake_3d_signals_5mhz_complex.copy()
    f_iqs3 = apply_wall_filter(iqs3, 'poly', degree, axis=-1)

    assert np.allclose(f_iqs1, f_iqs2)
    assert np.allclose(f_iqs1, f_iqs3)


def test_hp_wall_filter(fake_3d_signals_5mhz_complex):
    # Simply comparing to scipy
    deg = 1
    filtered = apply_wall_filter(fake_3d_signals_5mhz_complex, 'hp_filter', deg)
    w_n = deg / 10
    b, a = scipy.signal.butter(5, w_n, 'high')
    filtered_2 = scipy.signal.filtfilt(b, a, fake_3d_signals_5mhz_complex)
    assert np.allclose(filtered, filtered_2)

    # Another degree
    deg = 5
    filtered = apply_wall_filter(fake_3d_signals_5mhz_complex, 'hp_filter', deg)
    w_n = deg / 10
    b, a = scipy.signal.butter(5, w_n, 'high')
    filtered_2 = scipy.signal.filtfilt(b, a, fake_3d_signals_5mhz_complex)
    assert np.allclose(filtered, filtered_2)


def test_spatial_smoothing():
    # Test in an ones matrix, the smoothing should then be homogeneous. It will
    # also be tested on a real example below (doppler maps)
    result = spatial_smoothing(np.ones((10, 20)), 3)
    assert np.unique(result).size == 1
    hamming_matrix = np.hamming(3)[:, None] * np.hamming(3)
    assert (result == np.sum(hamming_matrix)).all()


def test_median_smoothing():
    # Test the complex version
    some_data = np.random.randn(10, 20)
    result = spatial_smoothing(some_data, 3, 'median')
    assert np.allclose(
        result, scipy.ndimage.median_filter(some_data, 3, mode='nearest'))
    some_data = some_data + 1j * np.random.randn(10, 20)
    result = spatial_smoothing(some_data, 3, 'median')
    assert np.allclose(
        result.real,
        scipy.ndimage.median_filter(some_data.real, 3, mode='nearest'))
    assert np.allclose(
        result.imag,
        scipy.ndimage.median_filter(some_data.imag, 3, mode='nearest'))


def test_color_map_doppler():
    # Compare our results with the ones obtained using MUST. Same as the tests
    # in test_das, we've seen that there are some approximations in the
    # computation, so we have to slightly increase the tolerance to 1e-5 (which
    # is acceptable).
    must_val = {
        'min': -0.6719156484358612,
        'max': 0.6940913779213181,
        'mean': -0.0074107905388399314,
    }
    tol = (must_val['max'] - must_val['min']) / 1e5
    lat_coords = [(145, 165), 203]
    axi_coords = [30, (80, 100)]
    lat = np.array([
        -0.14972894, -0.15777197, -0.16468393, -0.17145369, -0.1835298,
        -0.19328103, -0.20506856, -0.22145367, -0.23611773, -0.2481624,
        -0.26080097, -0.27289411, -0.27690535, -0.2725436, -0.26913766,
        -0.27209166, -0.28127949, -0.29079444, -0.28804362, -0.29212882])
    axi = np.array([
        0.5091089, 0.50734668, 0.50080807, 0.49527496, 0.49219058,
        0.4882372, 0.48390381, 0.48489489, 0.49306047, 0.49244194,
        0.49462069, 0.49697871, 0.49825599, 0.49999375, 0.50500063,
        0.51106599, 0.51652445, 0.52157209, 0.52503882, 0.52880475])

    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'rotating_disk.mat'), 'must')
    x = np.linspace(-12.5, 12.5, 251) * 1e-3
    z = np.linspace(10, 35, 251) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'none')
    info = beamformer.setups
    iqs = us.cpu.rf2iq(reader.data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    packet = beamformer.beamform_packet(iqs, scan)
    nyquist = info['sound_speed'] * info['prf'] / (4 * info['central_freq'])
    color_map = get_color_doppler_map(packet, nyquist)

    assert must_val['min'] == pytest.approx(np.min(color_map), abs=tol)
    assert must_val['max'] == pytest.approx(np.max(color_map), abs=tol)
    assert must_val['mean'] == pytest.approx(np.mean(color_map), abs=tol)
    c = lat_coords
    assert np.allclose(lat, color_map[c[0][0]:c[0][1], c[1]], atol=tol)
    c = axi_coords
    assert np.allclose(axi, color_map[c[0], c[1][0]:c[1][1]], atol=tol)


def test_smoothed_color_map_doppler():
    # Same as above but with smoothing.
    must_val = {
        'min': -0.5903520532025739,
        'max': 0.6058720575834684,
        'mean': -0.00821010389291073,
    }
    tol = (must_val['max'] - must_val['min']) / 1e6
    lat_coords = [(145, 165), 203]
    axi_coords = [30, (80, 100)]
    lat = np.array([
        -0.14565244, -0.15170244, -0.15932071, -0.16901759, -0.18066433,
        -0.19329877, -0.20572527, -0.21742528, -0.2286342, -0.23939844,
        -0.24912588, -0.25706066, -0.2629461, -0.26728262, -0.27102889,
        -0.27513856, -0.28021744, -0.28632185, -0.29289132, -0.29911942])
    axi = np.array([
        0.50417204, 0.50393459, 0.50357834, 0.50322254, 0.50299194,
        0.50306064, 0.5035698, 0.50460025, 0.50603604, 0.50764562,
        0.50918169, 0.51053088, 0.51173327, 0.51291229, 0.51417268,
        0.5156082, 0.51725164, 0.51912493, 0.52119611, 0.52343712])

    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'rotating_disk.mat'), 'must')
    x = np.linspace(-12.5, 12.5, 251) * 1e-3
    z = np.linspace(10, 35, 251) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'none')
    info = beamformer.setups
    iqs = us.cpu.rf2iq(reader.data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    packet = beamformer.beamform_packet(iqs, scan)
    nyquist = info['sound_speed'] * info['prf'] / (4 * info['central_freq'])
    color_map = get_color_doppler_map(packet, nyquist, kernel=11)

    assert must_val['min'] == pytest.approx(np.min(color_map), abs=tol)
    assert must_val['max'] == pytest.approx(np.max(color_map), abs=tol)
    assert must_val['mean'] == pytest.approx(np.mean(color_map), abs=tol)
    c = lat_coords
    assert np.allclose(lat, color_map[c[0][0]:c[0][1], c[1]], atol=tol)
    c = axi_coords
    assert np.allclose(axi, color_map[c[0], c[1][0]:c[1][1]], atol=tol)


def test_power_map_doppler():
    # Test the power map doppler.
    # Warning: Since there is a conversion to decibel, the small errors are
    # amplified, and since we have a few mismatching pixels, the tolerance here
    # is set to a very low level for the min value
    must_val = {
        'min': -55.34389305810913,
        'max': 0.0,
        'mean': -17.56497553957861,
    }
    min_tol = (must_val['max'] - must_val['min']) / 1e3
    tol = (must_val['max'] - must_val['min']) / 1e6
    lat_coords = [(145, 165), 203]
    axi_coords = [30, (80, 100)]
    lat = np.array([
        -7.21867753, -8.10918149, -9.32454929, -10.49953485,
        -11.01360447, -10.64967793, -10.15654437, -9.95844716,
        -10.22928744, -10.30377673, -10.36208787, -10.31845396,
        -9.79214889, -9.12906588, -8.89474432, -9.45782193,
        -10.54648569, -11.12954738, -10.12116939, -9.10870139])
    axi = np.array([
        -7.56262047, -7.68213839, -7.8925532, -8.28717717,
        -9.12174994, -9.7318951, -10.31734155, -10.60325127,
        -10.65497988, -10.1933339, -9.83258395, -9.62477739,
        -9.27356161, -8.64321749, -8.00003922, -7.44877926,
        -6.54615571, -5.60556823, -4.8488404, -4.17743872])

    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'rotating_disk.mat'), 'must')
    x = np.linspace(-12.5, 12.5, 251) * 1e-3
    z = np.linspace(10, 35, 251) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'none')
    info = beamformer.setups
    iqs = us.cpu.rf2iq(reader.data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    packet = beamformer.beamform_packet(iqs, scan)
    power_map = get_power_doppler_map(packet)

    assert must_val['min'] == pytest.approx(np.min(power_map), abs=min_tol)
    assert must_val['max'] == pytest.approx(np.max(power_map), abs=tol)
    assert must_val['mean'] == pytest.approx(np.mean(power_map), abs=tol)
    c = lat_coords
    assert np.allclose(lat, power_map[c[0][0]:c[0][1], c[1]], atol=tol)
    c = axi_coords
    assert np.allclose(axi, power_map[c[0], c[1][0]:c[1][1]], atol=tol)
