"""Unit test file for all the probes.
"""
import numpy as np
import pytest

from ultraspy.probes.factory import (get_probe, build_probe,
                                     build_probe_from_geometry)


def test_get_probe():
    probe = get_probe('L7-4')
    assert probe.central_freq == pytest.approx(5.208e6)
    assert probe.nb_elements == 128
    assert probe.geometry.shape == (3, probe.nb_elements)

    probe = get_probe('C5-2v')
    assert probe.get_thetas().any()


def test_build_probe():
    probe = build_probe('linear', 128, 0.298e-3, 5.208e6, 60)
    probe_l74 = get_probe('L7-4')
    assert np.allclose(probe.geometry, probe_l74.geometry)


def test_build_probe_from_geometry():
    probe = get_probe('MUX_1024_8MHz')
    copy_probe = build_probe_from_geometry(probe.geometry[0],
                                           probe.geometry[1],
                                           probe.geometry[2],
                                           probe.central_freq)
    assert np.allclose(probe.geometry, copy_probe.geometry)
