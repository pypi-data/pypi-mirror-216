"""Unit test file for all the scans.
"""
import numpy as np
import pytest

from ultraspy.scan import GridScan, PolarScan


def test_grid_scan():
    # Builds a standard 2D grid scan
    x = np.linspace(-10, 10, 50)
    z = np.linspace(0, 30, 100)
    scan = GridScan(x, z, on_gpu=False)
    assert len(scan.pixels) == 2
    assert np.all([p.shape == scan.pixels[0].shape for p in scan.pixels])
    assert scan.nb_x == x.size
    assert scan.nb_z == z.size
    assert np.array(scan.axial_step).size == 1
    assert scan.pixels[0][20, 10] == x[20]
    assert scan.pixels[1][20, 10] == z[10]
    scan.oversample_axial(4)
    assert scan.nb_z == z.size * 4
    scan.downsample_axial(2.2)
    assert scan.nb_z == z.size * 2
    assert scan.z_axis[0] == z[0]
    assert scan.z_axis[-1] == z[-1]

    # Builds a standard 3D grid scan
    y = np.linspace(-10, 10, 20)
    scan = GridScan(x, y, z, on_gpu=False)
    assert len(scan.pixels) == 3
    assert np.all([p.shape == scan.pixels[0].shape for p in scan.pixels])
    assert scan.nb_y == y.size
    assert np.array(scan.axial_step).size == 1
    assert scan.pixels[0][20, 5, 10] == x[20]
    assert scan.pixels[1][20, 5, 10] == y[5]
    assert scan.pixels[2][20, 5, 10] == z[10]


def test_polar_scan():
    # Builds a standard 2D grid scan
    r = np.linspace(0, 30, 100)
    p = np.linspace(np.radians(-45), np.radians(45), 50)
    scan = PolarScan(r, p, on_gpu=False)
    assert len(scan.pixels) == 2
    assert np.all([p.shape == scan.pixels[0].shape for p in scan.pixels])
    assert scan.nb_x == p.size
    assert scan.nb_z == r.size
    scan.oversample_axial(4)
    assert scan.nb_z == r.size * 4
    scan.downsample_axial(2.2)
    assert scan.nb_z == r.size * 2
    assert scan.z_rhos[0] == r[0]
    assert scan.z_rhos[-1] == r[-1]

    # Builds a standard 3D grid scan
    t = np.linspace(-10, 10, 20)
    scan = PolarScan(r, p, t, on_gpu=False)
    assert len(scan.pixels) == 3
    assert np.all([p.shape == scan.pixels[0].shape for p in scan.pixels])
    assert scan.nb_y == t.size


def test_fix_axis():
    # Builds a standard 2D grid scan
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    z = np.linspace(0, 30, 100)
    scan = GridScan(x, z, on_gpu=False)
    pixels = scan.pixels.copy()
    scan.fix_an_axis(0, 20)
    assert np.all(pixels == scan.pixels)

    scan = GridScan(x, y, z, on_gpu=False)
    with pytest.raises(NotImplementedError):
        scan.fix_an_axis(-1, 20)
    with pytest.raises(NotImplementedError):
        scan.fix_an_axis(2, 100)

    scan.fix_an_axis(0, 20)
    assert scan.pixels[0].shape == (1, scan.nb_y, scan.nb_z)
    assert scan.pixels[0][0, 0, 0] == scan.x_axis[20]
    scan.fix_an_axis(2, 40)
    assert scan.pixels[0].shape == (scan.nb_x, scan.nb_y, 1)
    assert scan.pixels[2][0, 0, 0] == scan.z_axis[40]

    scan.remove_fixed_axis()
    assert scan.pixels[0].shape == (scan.nb_x, scan.nb_y, scan.nb_z)


def test_boundaries():
    # Builds a standard 2D grid scan
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    z = np.linspace(0, 30, 100)
    scan = GridScan(x, z, on_gpu=False)
    assert scan.bounds[0][0] == pytest.approx(x[0])
    assert scan.bounds[0][1] == pytest.approx(x[-1])
    assert scan.bounds[1][0] == pytest.approx(z[0])
    assert scan.bounds[1][1] == pytest.approx(z[-1])

    scan = GridScan(x, y, z, on_gpu=False)
    assert scan.bounds[0][0] == pytest.approx(x[0])
    assert scan.bounds[0][1] == pytest.approx(x[-1])
    assert scan.bounds[1][0] == pytest.approx(y[0])
    assert scan.bounds[1][1] == pytest.approx(y[-1])
    assert scan.bounds[2][0] == pytest.approx(z[0])
    assert scan.bounds[2][1] == pytest.approx(z[-1])

    # Builds a standard 2D grid scan
    r = np.linspace(0, 30, 100)
    p = np.linspace(np.radians(-45), np.radians(45), 50)
    scan = PolarScan(r, p, on_gpu=False)
    min_x = r[-1] * np.sin(p[0])
    max_x = r[-1] * np.sin(p[-1])
    min_z = r[0] * np.cos(p[0])
    max_z = r[-1] * np.cos(0)
    assert scan.bounds[0][0] == pytest.approx(min_x)
    assert scan.bounds[0][1] == pytest.approx(max_x)
    assert scan.bounds[1][0] == pytest.approx(min_z)
    assert scan.bounds[1][1] == pytest.approx(max_z, rel=1e-3)
