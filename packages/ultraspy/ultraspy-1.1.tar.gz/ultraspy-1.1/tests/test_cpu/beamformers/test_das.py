"""Unit test file to test our DAS beamformer.
"""
import os
import numpy as np
import pytest

from ultraspy.io.reader import Reader
from ultraspy.scan import GridScan, PolarScan
from ultraspy.beamformers.das import DelayAndSum
from ultraspy.config import cfg
import ultraspy as us


def test_sta():
    # Compare our results with our own results, high-level
    vals = {
        'min': -363399.34,
        'max': 480629.16,
        'median': -492.51074,
        'mean': -494.8726,
    }
    tol = (vals['max'] - vals['min']) / 1e6
    scat_lat_coords = [(11, 31), 260]
    scat_axi_coords = [21, (250, 270)]
    scat_lat = np.array([
        5.4151196e+02, -6.5509479e+02, 1.7518591e+02, 9.9519226e+02,
        3.7315680e+02, 1.4579752e+03, -2.8391353e+03, -1.3245040e+04,
        8.1022500e+04, 3.6513444e+05, 4.8062916e+05, 2.4352280e+05,
        3.2953285e+04, -1.1075819e+04, -1.0147509e+04, -5.8044556e+03,
        -6.2120752e+02, -3.7445319e+02, 5.7632690e+02, 8.7417633e+02])
    scat_axi = np.array([
        -4373.5728, -7917.4233, -4817.7183, 35008.883,
        110726.95, 87216.35, -151626.56, -363399.34,
        -163352.7, 313331.44, 480629.16, 118213.27,
        -327028.12, -360727.22, -16208.817, 272162.94,
        201389.89, -93905., -246179.53, -97404.805])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'pa2_sta.mat'), 'dbsas')
    x = np.linspace(0, 10, 50) * 1e-3
    z = np.linspace(40, 50, 400) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_setup('sound_speed', 1440)
    beamformer.update_option('reduction', 'sum')

    # Only select a few transmissions, for faster computation
    transmissions_indices = list(range(64, 96, 3))
    data = reader.data[0, transmissions_indices]
    beamformer.update_setup('transmissions_idx', transmissions_indices)

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(vals['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(vals['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(vals['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(vals['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]],
                       atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]],
                       atol=tol)


def test_das_none_rfs():
    # Compare our results with the ones obtained using MUST. Note, that MUST
    # has been updated in dasmtx (computation of dTX), we've removed the
    # interpolation by 4, simply doing:
    # -> dTX = min(delaysTX*c + sqrt((xe-x).^2 + (ze-z).^2),[],2);
    must_val = {
        'min': -26.929600313305855,
        'max': 29.73177061090246,
        'median': 0.0,
        'mean': -0.00012563729829199614,
    }
    tol = (must_val['max'] - must_val['min']) / 1e6
    scat_lat_coords = [(175, 195), 338]
    scat_axi_coords = [186, (330, 350)]
    scat_lat = np.array([
        -5.99874785e-01, -4.78659099e-01, -2.49031908e-02, -1.08810168e+00,
        3.21182155e-01, -3.75227740e+00, -6.12309946e+00, -2.95718508e+00,
        5.23576750e+00, 9.45794010e+00, 1.62769330e+01, 2.23987275e+01,
        2.64162241e+01, 2.43780449e+01, 1.90447695e+01, 1.04151076e+01,
        2.79689184e+00, 5.61388958e-01, -2.46372467e+00, -4.52067520e+00])
    scat_axi = np.array([
        0.31287642, 7.13840971, -2.5494524, -12.79438565,
        7.64946625, 15.57467772, -17.03544702, -12.58661607,
        22.39872748, 4.19336934, -18.76905089, 4.62832323,
        9.57883145, -4.4903496, -3.01221348, 2.02411864,
        -0.03301438, 0.11225692, -1.09376434, -1.62738756])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'none')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_linear_rfs():
    # Same as above but with linear interpolation
    must_val = {
        'min': -24.461327986496876,
        'max': 28.223172952342278,
        'median': 0.0,
        'mean': -0.0001294976356010244,
    }
    tol = (must_val['max'] - must_val['min']) / 1e6
    scat_lat_coords = [(175, 195), 338]
    scat_axi_coords = [186, (330, 350)]
    scat_lat = np.array([
        -0.08874402, 0.20795811, 0.49796621, 0.28822708, -1.27845785,
        -3.04109748, -3.34402311, -1.69214157, 2.64612879, 8.77361387,
        15.21548402, 20.79774185, 23.13717716, 21.37999706, 16.47976891,
        9.70350168, 3.77236528, -0.31762235, -2.46794873, -2.82333219])
    scat_axi = np.array([
        2.42441989e-01, 5.87331335e+00, -2.01063371e+00, -1.15802002e+01,
        8.09829808e+00, 1.49748703e+01, -1.67141439e+01, -1.19784216e+01,
        2.07977418e+01, 3.13556655e+00, -1.73514429e+01, 3.17072648e+00,
        9.42451293e+00, -3.96150632e+00, -3.21251199e+00, 1.50094949e+00,
        6.07853820e-01, -1.78846778e-01, 1.79762514e-02, -4.66720892e-01])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_linear_fnb0_rfs():
    # Same as above but with an f-number equal to 0 (full aperture)
    must_val = {
        'min': -37.99256642954093,
        'max': 38.46165199759746,
        'median': 0.0,
        'mean': -0.00021420842281738873,
    }
    tol = (must_val['max'] - must_val['min']) / 1e6
    scat_lat_coords = [(175, 195), 338]
    scat_axi_coords = [186, (330, 350)]
    scat_lat = np.array([
        -1.33101581, -1.05350752, -0.25416728, 1.35024768, 1.73369859,
        0.77639141, -1.90949425, -4.93988975, -3.90168537, 3.5913883,
        16.35358075, 27.04660436, 29.85639002, 23.65618026, 13.06362997,
        4.75123868, 0.49457438, -0.58870509, -0.52586464, -1.00774264])
    scat_axi = np.array([
        1.62446349, 5.46165636, -4.83357753, -12.08764171,
        12.92154473, 16.12149922, -22.6350452, -13.55363439,
        27.04660436, 4.93260019, -22.66780057, 1.82748757,
        12.76491117, -2.98887866, -4.85976436, 0.87964121,
        1.16697687, 0.15026574, -0.03452026, -0.56117173])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 0.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_linear_fnb5_rfs():
    # Same as above but with an f-number equal to 5 (absurdly small aperture)
    must_val = {
        'min': -6.218378857471024,
        'max': 7.0152697618211795,
        'median': 0.0,
        'mean': -0.00011792426177914833,
    }
    tol = (must_val['max'] - must_val['min']) / 1e6
    scat_lat_coords = [(175, 195), 338]
    scat_axi_coords = [186, (330, 350)]
    scat_lat = np.array([
        1.78006848, 2.05414849, 2.3255261, 3.02094613, 3.51183267,
        3.73528865, 4.0060779, 4.47896579, 4.88408353, 4.94221009,
        5.0876554, 5.19557464, 5.25806061, 5.22034263, 5.21769225,
        4.96883858, 4.71141785, 4.5132888, 4.36542217, 3.90042921])
    scat_axi = np.array([
        -0.13673622, 1.50984904, -0.13042056, -3.04670003, 1.75208356,
        3.73708867, -4.06497558, -2.41915863, 5.19557464, -0.09116807,
        -4.12487779, 1.32584902, 1.65831515, -1.39275587, -0.65651145,
        0.25050279, 0.40728308, -0.13451018, -0.26765859, -0.01986047])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 5.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_mean():
    # TODO: test delay and mean
    assert True


def test_das_convex_fnb0():
    # Test some simulation data acquired with a convex probe, comparison with
    # MUST, but still some approximations, so we've set the tolerance to 1e-5,
    # still acceptable
    must_val = {
        'min': -17687.689272347554,
        'max': 14634.420636567507,
        'median': 0.07947856639536374,
        'mean': -0.08103513061901287,
    }
    tol = (must_val['max'] - must_val['min']) / 1e5
    scat_lat_coords = [(264, 284), 714]
    scat_axi_coords = [274, (704, 724)]
    scat_lat = np.array([
        -255.20040076, 492.57028664, 1033.07623606, 1098.16268371,
        482.6444815, -1720.41430721, -5354.81518185, -9302.17326185,
        -12981.5438865, -15790.14930923, -17288.73588489, -17598.23878656,
        -15971.6423468, -13066.08170589, -9090.90315834, -4845.5079416,
        -1162.51442097, 1093.87097093, 1684.23208163, 1340.70529459])
    scat_axi = np.array([
        -1866.61564744, -4517.74196871, -5855.38003685, -6029.28882017,
        -2517.06141023, 4053.54775155, 12367.53046081, 14182.10982777,
        7249.14163777, -7435.64167505, -17288.73588489, -16379.97697662,
        -4056.91984409, 7931.09110363, 13100.21565861, 9419.86537279,
        2877.54013059, -2801.49671653, -5195.88131738, -5190.36289504])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    data_name = 'simu_convex_scatterers.mat'
    reader = Reader(os.path.join(rsc_dir, data_name), 'simus')

    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 40, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    data = reader.data[0]
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 0.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_convex_fnb5():
    # Test some simulation data acquired with a convex probe, comparison with
    # MUST -> Tol = 5 WARNING
    must_val = {
        'min': -4438.898009541836,
        'max': 3773.022140012065,
        'median': 0.0,
        'mean': 0.007575127896463454,
    }
    tol = (must_val['max'] - must_val['min']) / 1e5
    scat_lat_coords = [(264, 284), 714]
    scat_axi_coords = [274, (704, 724)]
    scat_lat = np.array([
        -3117.48430971, -3680.02513179, -3680.97233111, -3679.32002875,
        -3653.78342623, -3619.01170677, -3023.62980911, -3010.61233604,
        -3006.42451973, -2980.26717813, -3160.42052243, -3126.4030426,
        -3050.91243666, -2984.45951057, -2927.04745102, -2550.74097733,
        -2563.89255702, -2589.77976366, -2595.022503, -2829.83416027])
    scat_axi = np.array([
        267.59558252, -241.41717969, -883.03323274, -1606.56390917,
        -1724.28398361, -685.56409738, 1730.92423036, 3576.21151967,
        3138.37127936, 159.61638279, -3160.42052243, -4005.38002258,
        -2384.38687392, 626.87707244, 2249.47946535, 2750.14787688,
        1612.32121397, 404.00405175, -1162.02382553, -1782.62793615])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    data_name = 'simu_convex_scatterers.mat'
    reader = Reader(os.path.join(rsc_dir, data_name), 'simus')

    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 40, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    data = reader.data[0]
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 5.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')
    beamformer.update_option('emitted_aperture', False)

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_linear_fnb1_iqs():
    # Same as above but with a regular f-number and on I/Qs
    must_rval = {
        'min': -30.320398444964248,
        'max': 33.635619265218644,
        'median': -4.3477484709195995e-05,
        'mean': 5.204721178463003e-28,
    }
    must_ival = {
        'min': -29.419154940496444,
        'max': 33.83175004224053,
        'median': -1.143704796352504e-05,
        'mean': 4.564857648625526e-28,
    }
    rtol = (must_rval['max'] - must_rval['min']) / 1e6
    itol = (must_ival['max'] - must_ival['min']) / 1e6
    scat_lat_coords = [(175, 195), 338]
    scat_axi_coords = [186, (330, 350)]
    scat_lat = np.array([
        0.45811804 - 0.9598892j, 1.0429939 - 1.11519817j,
        0.95062921 - 0.77816607j, 0.49330518 + 0.17210901j,
        -1.1077939 + 1.2316905j, -3.03512095 + 2.19795664j,
        -3.53586831 + 2.50100776j, -2.24394281 + 1.733725j,
        2.95164667 - 0.20624597j, 10.37324746 - 3.04770015j,
        18.39705263 - 6.24586863j, 25.34793964 - 8.81899364j,
        27.66740675 - 10.20898584j, 25.64567996 - 9.68789848j,
        19.62255819 - 7.2909088j, 11.91733153 - 3.69662278j,
        4.74716917 - 0.59866671j, -0.44677219 + 1.76207927j,
        -3.0024057 + 2.58208099j, -3.25162879 + 2.0674912j])
    scat_axi = np.array([
        -0.11453108 - 4.2010215j, 7.08561149 + 0.30648583j,
        -1.68914094 + 10.66297866j, -14.32686444 - 4.45954646j,
        8.67975547 - 17.18616582j, 18.59525465 + 14.25220415j,
        -19.51852129 + 17.6637549j, -14.0779756 - 23.58017048j,
        25.34793964 - 8.81899364j, 3.15142505 + 24.38459545j,
        -20.99094205 - 1.65152923j, 4.70450532 - 16.09475311j,
        10.90259 + 5.7615648j, -5.20223581 + 6.45840077j,
        -3.27920084 - 3.77996341j, 2.21377212 - 1.37455693j,
        0.43474775 + 0.98599429j, -0.22446592 + 0.03984444j,
        0.10024727 + 0.18310669j, -0.37296796 + 0.10910072j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=200)
    beamformed = beamformer.beamform(iqs, scan)

    real = beamformed.real
    imag = beamformed.imag
    assert np.min(real) == pytest.approx(must_rval['min'], abs=rtol)
    assert np.max(real) == pytest.approx(must_rval['max'], abs=rtol)
    assert np.median(real) == pytest.approx(must_rval['median'], abs=rtol)
    assert np.mean(real) == pytest.approx(must_rval['mean'], abs=rtol)
    assert np.min(imag) == pytest.approx(must_ival['min'], abs=itol)
    assert np.max(imag) == pytest.approx(must_ival['max'], abs=itol)
    assert np.median(imag) == pytest.approx(must_ival['median'], abs=itol)
    assert np.mean(imag) == pytest.approx(must_ival['mean'], abs=itol)
    tol = min(rtol, itol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_linear_fnb1_iqs_with_t0():
    # Same as above but with an artificial t0. The precision is a bit lower
    # than other operations, but the use of t0 to rotate the phase might be the
    # reason of this approximation. Set the tol to 1e-5 * max-to-min, instead
    # of 1e-6. Acceptable.
    must_rval = {
        'min': -12.123253216083764,
        'max': 11.610992034965065,
        'median': -3.161532400194281e-05,
        'mean': 0.0,
    }
    must_ival = {
        'min': -11.219090928430013,
        'max': 11.750490396721315,
        'median': -2.8243202860574954e-05,
        'mean': 0.0,
    }
    rtol = (must_rval['max'] - must_rval['min']) / 1e5
    itol = (must_ival['max'] - must_ival['min']) / 1e5
    scat_lat_coords = [(190, 210), 822]
    scat_axi_coords = [200, (810, 830)]
    scat_lat = np.array([
        1.90796014 + 6.51025866j, 3.72535086 + 5.84569934j,
        5.26574612 + 4.70790353j, 6.42436244 + 3.21927705j,
        7.16136699 + 1.43943893j, 7.38953893 - 0.46098284j,
        7.12713129 - 2.32365661j, 6.40042845 - 4.03244135j,
        5.24241631 - 5.53443781j, 3.78949007 - 6.68975791j,
        2.14079106 - 7.4448431j, 0.39252367 - 7.76747903j,
        -1.40781925 - 7.68694766j, -3.09383446 - 7.20944968j,
        -4.57706446 - 6.39869545j, -5.82665903 - 5.29609286j,
        -6.81464659 - 3.94990506j, -7.46990338 - 2.48768105j,
        -7.80416321 - 0.98209894j, -7.82698079 + 0.55696024j])
    scat_axi = np.array([
        0.09809378 - 0.12113324j, 0.14269338 - 0.01260811j,
        0.23414335 + 0.17846189j, -0.27206864 + 0.61007791j,
        -1.1635337 - 0.50908276j, 1.00944889 - 1.85046101j,
        2.53858927 + 1.87137151j, -3.1190733 + 3.00486212j,
        -3.01983864 - 4.62834204j, 6.13476426 - 2.41634374j,
        1.19557518 + 7.29078885j, -7.7766111 - 0.43879905j,
        2.14079106 - 7.4448431j, 6.3489892 + 3.49713881j,
        -4.22256493 + 4.7707607j, -3.0871496 - 4.23066588j,
        3.65229412 - 1.65605037j, 0.68839687 + 2.7534023j,
        -1.81813548 + 0.18231386j, -0.02143603 - 1.05530318j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [37]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('t0', 35e-6)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    beamformed = beamformer.beamform(iqs, scan)

    real = beamformed.real
    imag = beamformed.imag
    assert np.min(real) == pytest.approx(must_rval['min'], abs=rtol)
    assert np.max(real) == pytest.approx(must_rval['max'], abs=rtol)
    assert np.median(real) == pytest.approx(must_rval['median'], abs=rtol)
    assert np.mean(real) == pytest.approx(must_rval['mean'], abs=rtol)
    assert np.min(imag) == pytest.approx(must_ival['min'], abs=itol)
    assert np.max(imag) == pytest.approx(must_ival['max'], abs=itol)
    assert np.median(imag) == pytest.approx(must_ival['median'], abs=itol)
    assert np.mean(imag) == pytest.approx(must_ival['mean'], abs=itol)
    tol = min(rtol, itol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_linear_plane_waves_rfs():
    # Same as above but with linear interpolation
    must_val = {
        'min': -66.454009206561,
        'max': 72.830491947969,
        'median': -9.512777132298759e-05,
        'mean': 0.0,
    }
    tol = (must_val['max'] - must_val['min']) / 1e6
    scat_lat_coords = [(175, 195), 338]
    scat_axi_coords = [186, (330, 350)]
    scat_lat = np.array([
        -0.43312082, 0.90801096, 1.23730396, 1.368233, 1.22898557,
        1.49976464, 1.5779457, 0.662316, 2.13295599, 11.51700975,
        29.67063404, 50.39736113, 60.97626685, 55.17262143, 36.50915418,
        16.62517624, 4.37323498, 1.14113119, 2.05222097, 2.05008164])
    scat_axi = np.array([
        2.26610622, 15.19332067, -7.9173643, -29.34741815,
        22.17904373, 37.42181702, -40.39390499, -30.56746167,
        50.39736113, 12.78470475, -43.78785048, 0.84982472,
        24.50278448, -4.74274821, -9.2377169, 2.17665814,
        2.61961546, 0.23052119, -0.79361554, -0.331031])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [0, 37, 74]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')
    beamformer.update_option('interpolation', 'linear')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    assert np.min(beamformed) == pytest.approx(must_val['min'], abs=tol)
    assert np.max(beamformed) == pytest.approx(must_val['max'], abs=tol)
    assert np.median(beamformed) == pytest.approx(must_val['median'], abs=tol)
    assert np.mean(beamformed) == pytest.approx(must_val['mean'], abs=tol)
    c = scat_lat_coords
    assert np.allclose(scat_lat, beamformed[c[0][0]:c[0][1], c[1]], atol=tol)
    c = scat_axi_coords
    assert np.allclose(scat_axi, beamformed[c[0], c[1][0]:c[1][1]], atol=tol)


def test_das_3d_rfs():
    # Test the 3d DAS on regular configuration. Comparison is high level, made
    # with visual verification, no comparison with external tool such as MUST
    vals = {
        'min': -8.389495213740741e-24,
        'max': 6.8988303362044e-24,
        'median': -1.4277873044906783e-38,
        'mean': 3.9177963227685826e-27,
    }
    tol = (vals['max'] - vals['min']) / 1e6
    scat_lat_coords = [(0, 10), 5, 25]
    scat_elev_coords = [5, (0, 10), 25]
    scat_axi_coords = [5, 5, (20, 30)]
    scat_lat = np.array([
        -2.95820186e-25, 3.05634459e-25, 1.84755625e-24, 3.98243098e-24,
        5.80337642e-24, 6.88529829e-24, 6.62696131e-24, 5.10000550e-24,
        3.15326493e-24, 1.56694069e-24])
    scat_elev = np.array([
        6.88322504e-26, 1.81854329e-24, 3.85238372e-24, 6.15768156e-24,
        6.88529829e-24, 6.88529829e-24, 6.15768156e-24, 3.85238372e-24,
        1.81854329e-24, 6.88322504e-26])
    scat_axi = np.array([
        1.52112647e-24, -2.51666487e-24, -2.11096612e-25, 5.46947987e-24,
        -8.32627333e-24, 6.88529829e-24, -2.72009398e-24, -1.66778643e-24,
        2.23782913e-24, -8.09012151e-26])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [2]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'none')

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


def test_das_3d_fnb5_rfs():
    # Same as above but with fnb = 5
    vals = {
        'min': -2.413586142069319e-24,
        'max': 1.9866622278055274e-24,
        'median': -3.724219501229528e-39,
        'mean': 1.501606194349856e-28,
    }
    tol = (vals['max'] - vals['min']) / 1e6
    scat_lat_coords = [(0, 10), 5, 25]
    scat_elev_coords = [5, (0, 10), 25]
    scat_axi_coords = [5, 5, (20, 30)]
    scat_lat = np.array([
        1.08276149e-24, 1.33156018e-24, 1.57674166e-24, 1.71343043e-24,
        1.85485073e-24, 1.85833117e-24, 1.91187000e-24, 1.87427255e-24,
        1.49828736e-24, 1.30467463e-24])
    scat_elev = np.array([
        1.09965000e-24, 1.55588842e-24, 1.57280539e-24, 1.71089076e-24,
        1.85833117e-24, 1.85833117e-24, 1.71089076e-24, 1.57280539e-24,
        1.55588842e-24, 1.09965000e-24])
    scat_axi = np.array([
        4.11673426e-25, -5.34654750e-25, -3.73277682e-25, 1.83934841e-24,
        -2.35040115e-24, 1.85833117e-24, -8.02830251e-25, -5.91078438e-25,
        8.75303310e-25, -2.05867423e-25])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [2]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 5.)
    beamformer.update_option('interpolation', 'none')

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


def test_das_3d_iqs():
    # Same but on I/Qs
    rvals = {
        'min': -8.851010811831803e-24,
        'max': 7.574311888672616e-24,
        'median': -5.428044723781732e-28,
        'mean': 1.312197057653364e-29,
    }
    ivals = {
        'min': -6.4672274200221266e-24,
        'max': 6.5615996896173734e-24,
        'median': 6.732586546582364e-28,
        'mean': -5.651465885374032e-29,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(0, 10), 5, 25]
    scat_elev_coords = [5, (0, 10), 25]
    scat_axi_coords = [5, 5, (20, 30)]
    scat_lat = np.array([
        -1.93005381e-25 - 1.15808575e-24j, 4.12561336e-25 - 3.26021890e-24j,
        2.04903970e-24 - 5.13197765e-24j, 4.37306870e-24 - 5.91395944e-24j,
        6.47875308e-24 - 5.30082698e-24j, 7.57431189e-24 - 3.39449432e-24j,
        7.12259600e-24 - 1.23414471e-24j, 5.45366322e-24 + 3.17305561e-25j,
        3.35825348e-24 + 8.18204844e-25j, 1.72636039e-24 + 3.34248016e-25j])
    scat_elev = np.array([
        -4.19456887e-26 - 5.04453087e-25j, 1.86232234e-24 - 1.26962480e-24j,
        4.16939114e-24 - 2.23155458e-24j, 6.24090529e-24 - 3.04184145e-24j,
        7.57431189e-24 - 3.39449432e-24j, 7.57431189e-24 - 3.39449432e-24j,
        6.24090529e-24 - 3.04184145e-24j, 4.16939114e-24 - 2.23155458e-24j,
        1.86232234e-24 - 1.26962480e-24j, -4.19456887e-26 - 5.04453087e-25j])
    scat_axi = np.array([
        2.14107358e-24 - 6.23919716e-25j, -2.27722163e-24 + 3.69989040e-24j,
        -6.84728229e-25 - 6.46722742e-24j, 5.51127337e-24 + 6.06011419e-24j,
        -8.66661473e-24 - 1.86761743e-24j, 7.57431189e-24 - 3.39449432e-24j,
        -3.13749135e-24 + 5.84756803e-24j, -1.11563010e-24 - 4.31309889e-24j,
        2.37984717e-24 + 9.14020266e-25j, -8.63223969e-25 + 1.27594375e-24j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [2]
    data = reader.data[0, pw]
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])

    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'none')

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


def test_das_3d_lat_pw_iqs():
    # Same as above with lateral plane waves
    rvals = {
        'min': -3.1059842518324145e-23,
        'max': 2.8718938878094713e-23,
        'median': 3.888463169709667e-28,
        'mean': 8.391931291119102e-28,
    }
    ivals = {
        'min': -2.2968349405871554e-23,
        'max': 2.519409001322206e-23,
        'median': 2.7963823540949806e-27,
        'mean': 6.815683352685715e-28,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(0, 10), 5, 25]
    scat_elev_coords = [5, (0, 10), 25]
    scat_axi_coords = [5, 5, (20, 30)]
    scat_lat = np.array([
        -1.57769079e-24 - 1.12669649e-24j, -2.65318052e-24 - 4.99432893e-24j,
        -3.04979223e-25 - 1.34086784e-23j, 9.22239813e-24 - 2.11962925e-23j,
        2.21994521e-23 - 2.03868742e-23j, 2.87189389e-23 - 9.90392085e-24j,
        2.37194141e-23 + 1.46374814e-24j, 1.27978696e-23 + 5.77912131e-24j,
        4.36297217e-24 + 3.92335071e-24j, 8.76466920e-25 + 1.13515880e-24j])
    scat_elev = np.array([
        3.20521956e-26 - 1.54221835e-24j, 7.32872542e-24 - 3.70792005e-24j,
        1.60276128e-23 - 6.56153911e-24j, 2.38570113e-23 - 9.00016203e-24j,
        2.87189389e-23 - 9.90392085e-24j, 2.87189389e-23 - 9.90392085e-24j,
        2.38570113e-23 - 9.00016203e-24j, 1.60276128e-23 - 6.56153911e-24j,
        7.32872542e-24 - 3.70792005e-24j, 3.20521956e-26 - 1.54221835e-24j])
    scat_axi = np.array([
        8.26945940e-24 - 7.13849865e-25j, -1.00653997e-23 + 1.16771827e-23j,
        6.91146485e-25 - 2.29683494e-23j, 1.67938743e-23 + 2.36746515e-23j,
        -3.02049202e-23 - 9.84266726e-24j, 2.87189389e-23 - 9.90392085e-24j,
        -1.35700903e-23 + 2.14425880e-23j, -3.27230007e-24 - 1.81413292e-23j,
        1.04488056e-23 + 5.78463688e-24j, -6.59155299e-24 + 4.41706458e-24j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [0, 1, 2, 3, 4]
    data = reader.data[0, pw]
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'none')

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


def test_das_3d_elev_pw_iqs():
    # Same but with elevational plane waves
    rvals = {
        'min': -3.122479202337641e-23,
        'max': 2.7717261394896214e-23,
        'median': 9.03193711209801e-29,
        'mean': 3.0592033832609685e-28,
    }
    ivals = {
        'min': -2.4653796603744346e-23,
        'max': 2.6273225319439842e-23,
        'median': 1.297960445435653e-27,
        'mean': -2.7164609354926846e-28,
    }
    rtol = (rvals['max'] - rvals['min']) / 1e6
    itol = (ivals['max'] - ivals['min']) / 1e6
    scat_lat_coords = [(0, 10), 5, 25]
    scat_elev_coords = [5, (0, 10), 25]
    scat_axi_coords = [5, 5, (20, 30)]
    scat_lat = np.array([
        -2.75118038e-25 - 3.92603041e-24j, 3.46443561e-24 - 1.06219613e-23j,
        1.05898087e-23 - 1.56109587e-23j, 1.91711535e-23 - 1.63574235e-23j,
        2.56941507e-23 - 1.25588914e-23j, 2.77172614e-23 - 5.31361928e-24j,
        2.43311568e-23 + 1.31079939e-24j, 1.75645224e-23 + 4.79927515e-24j,
        1.04859537e-23 + 4.64203755e-24j, 5.72333802e-24 + 1.83315223e-24j])
    scat_elev = np.array([
        -3.27196679e-26 - 1.58311486e-25j, 2.40155756e-24 - 2.14611993e-24j,
        9.45816209e-24 - 4.39180282e-24j, 1.97046202e-23 - 5.43724482e-24j,
        2.77172614e-23 - 5.31361928e-24j, 2.77172614e-23 - 5.31361928e-24j,
        1.97046202e-23 - 5.43724482e-24j, 9.45816209e-24 - 4.39180282e-24j,
        2.40155756e-24 - 2.14611993e-24j, -3.27196679e-26 - 1.58311486e-25j])
    scat_axi = np.array([
        9.08658063e-24 - 8.28184978e-25j, -1.17567799e-23 + 1.24304194e-23j,
        2.69642368e-24 - 2.46537966e-23j, 1.49782523e-23 + 2.62732253e-23j,
        -2.85674007e-23 - 1.33360172e-23j, 2.77172614e-23 - 5.31361928e-24j,
        -1.42385886e-23 + 1.56791571e-23j, 6.05437749e-26 - 1.26534540e-23j,
        4.77484268e-24 + 2.99726836e-24j, -9.38214818e-25 + 3.16960081e-24j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [5, 6, 2, 7, 8]
    data = reader.data[0, pw]
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'none')

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


def test_das_3d_both_pw_iqs():
    # Compare our results with what we want to obtain (high level with visual
    # verification, no comparison with external tool such as MUST)
    rvals = {
        'min': -7.214437809007293e-23,
        'max': 6.652170339841293e-23,
        'median': -2.5057138755671414e-27,
        'mean': 1.0802205226497432e-27,
    }
    ivals = {
        'min': -5.738208038827731e-23,
        'max': 6.15960082475142e-23,
        'median': 5.7239074136078624e-27,
        'mean': 9.215318912098969e-28,
    }
    # TODO: the tolerance is of 1e5 (instead of standard 1e6), because of the
    #       max values, this should be checked someday
    rtol = (rvals['max'] - rvals['min']) / 1e5
    itol = (ivals['max'] - ivals['min']) / 1e5
    scat_lat_coords = [(0, 10), 5, 25]
    scat_elev_coords = [5, (0, 10), 25]
    scat_axi_coords = [5, 5, (20, 30)]
    scat_lat = np.array([
        -2.20267660e-24 - 5.04459594e-24j, 2.37981794e-25 - 1.57180055e-23j,
        1.17011688e-23 - 3.05913452e-23j, 3.41938198e-23 - 3.98929502e-23j,
        5.76685486e-23 - 3.32870282e-23j, 6.65217034e-23 - 1.23315057e-23j,
        5.44971692e-23 + 7.60737038e-24j, 3.21031439e-23 + 1.43807302e-23j,
        1.37286741e-23 + 9.90027389e-24j, 4.78451682e-24 + 3.05954686e-24j])
    scat_elev = np.array([
        3.33513979e-25 - 1.47131254e-24j, 1.01649786e-23 - 5.47463041e-24j,
        2.83452719e-23 - 9.76694288e-24j, 5.05484952e-23 - 1.22616369e-23j,
        6.65217034e-23 - 1.23315057e-23j, 6.65217034e-23 - 1.23315057e-23j,
        5.05484952e-23 - 1.22616369e-23j, 2.83452719e-23 - 9.76694288e-24j,
        1.01649786e-23 - 5.47463041e-24j, 3.33513979e-25 - 1.47131254e-24j])
    scat_axi = np.array([
        2.19322628e-23 - 1.46334678e-24j, -2.78899258e-23 + 2.86136075e-23j,
        6.75510851e-24 - 5.73820804e-23j, 3.45042807e-23 + 6.15960082e-23j,
        -6.71528513e-23 - 3.17344229e-23j, 6.65217034e-23 - 1.23315057e-23j,
        -3.57264160e-23 + 3.88528761e-23j, 1.31610221e-24 - 3.43034002e-23j,
        1.33327417e-23 + 1.21705251e-23j, -7.46006953e-24 + 4.79423171e-24j])

    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'simu_3d_scatterers.mat'), 'simu_3d')
    x = np.linspace(1.5, 2.5, 10) * 1e-3
    y = np.linspace(-0.5, 0.5, 10) * 1e-3
    z = np.linspace(24, 26, 50) * 1e-3
    scan = GridScan(x, y, z, on_gpu=False)
    beamformer = DelayAndSum(is_iq=True, on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    data = reader.data[0]
    info = beamformer.setups
    iqs = us.cpu.rf2iq(data, info['central_freq'], info['sampling_freq'],
                       beamformer.t0, bandwidth=info['bandwidth'])
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('interpolation', 'none')

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


def test_das_polar():
    # TODO
    assert PolarScan


def test_das_no_compounding_sum():
    # Compare our results with or without compounding
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    pw = [0, 37, 74]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)
    beamformer.update_setup('signal_duration', 0)
    beamformer.update_setup('f_number', 1.)
    beamformer.update_option('reduction', 'sum')

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    # Same with no compounding
    beamformer.update_option('compound', False)
    beamformed_wo_compound = beamformer.beamform(data, scan)

    # Same with no reduce
    beamformer.update_option('reduce', False)
    beamformed_wo_reduce = beamformer.beamform(data, scan)

    # Same with compounding but no reduce
    beamformer.update_option('compound', True)
    beamformed_compound_no_reduce = beamformer.beamform(data, scan)

    vmax = min(np.max(beamformed), np.max(beamformed_wo_compound))
    vmin = max(np.min(beamformed), np.min(beamformed_wo_compound))
    tol = (vmax - vmin) / 1e6
    _, nb_t, nb_re = beamformer.received_probe.shape
    nb_x, nb_z = len(x), len(z)
    assert beamformed.ndim == 2
    assert beamformed_wo_compound.ndim == 3
    assert beamformed_wo_reduce.ndim == 4
    assert beamformed_compound_no_reduce.ndim == 3
    assert beamformed.shape == (nb_x, nb_z)
    assert beamformed_wo_compound.shape == (nb_t, nb_x, nb_z)
    assert beamformed_wo_reduce.shape == (nb_t, nb_re, nb_x, nb_z)
    assert beamformed_compound_no_reduce.shape == (nb_re, nb_x, nb_z)
    assert np.allclose(
        beamformed, np.sum(beamformed_wo_compound, axis=0), atol=tol)
    assert np.allclose(
        beamformed, np.sum(beamformed_wo_reduce, axis=(0, 1)), atol=tol)
    assert np.allclose(
        beamformed, np.sum(beamformed_compound_no_reduce, axis=0), atol=tol)


def test_das_no_compounding_mean():
    # Compare our results with or without compounding
    # Get the data
    rsc_dir = cfg.PATHS_RESOURCES
    reader = Reader(os.path.join(rsc_dir, 'picmus_simu_rfs.hdf5'), 'picmus')
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3
    scan = GridScan(x, z, on_gpu=False)
    beamformer = DelayAndSum(on_gpu=False)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)
    beamformer.update_option('reduction', 'mean')
    beamformer.update_option('compound', False)
    pw = [0, 37, 74]
    data = reader.data[0, pw]
    beamformer.update_setup('transmissions_idx', pw)

    # Beamformed
    beamformed = beamformer.beamform(data, scan)

    # Separated transmissions
    beamformer.update_option('compound', True)
    beamformer.update_setup('transmissions_idx', [pw[0]])
    beamformed_tr1 = beamformer.beamform(reader.data[0, [pw[0]]], scan)
    beamformer.update_setup('transmissions_idx', [pw[1]])
    beamformed_tr2 = beamformer.beamform(reader.data[0, [pw[1]]], scan)
    beamformer.update_setup('transmissions_idx', [pw[2]])
    beamformed_tr3 = beamformer.beamform(reader.data[0, [pw[2]]], scan)

    assert np.allclose(beamformed[0], beamformed_tr1)
    assert np.allclose(beamformed[1], beamformed_tr2)
    assert np.allclose(beamformed[2], beamformed_tr3)
