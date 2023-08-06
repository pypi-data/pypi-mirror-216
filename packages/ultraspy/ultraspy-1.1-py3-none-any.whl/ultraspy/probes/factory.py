"""Factory to get a probe based on its name or on some characteristics.
"""
import os
import json
import configparser

from .linear_probe import LinearProbe
from .convex_probe import ConvexProbe
from .matricial_probe import MatricialProbe

from ultraspy.config import cfg


available_probes = [
    'l7-4',
    'l11-4v',
    'l11-5v',
    'l14-5w',
    'c5-2v',
    'p4-2v',
    'mux_1024_8mhz',
]


def get_probe(probe_name):
    """Factory to load a probe configuration file within a class that will be
    used to properly compute the delays and probe elements positions.

    :param str probe_name: The name of the probe, needs to be picked among
        ::code::`probes.factory.available_probes`

    :returns: The Probe class with the main info (central freq, coordinates of
        elements, etc)
    :return type: LinearProbe, ConvexProbe, MatricialProbe
    """
    probe_name = probe_name.lower()
    assert probe_name in available_probes, \
        f"Unknown probe, please pick one of {available_probes}"

    # Load the ini config file
    config = configparser.ConfigParser()
    config.read(os.path.join(cfg.PATHS_PROBES, probe_name + '.ini'))

    # Get the geometry type
    geometry_type = config.get('General', 'type')

    # Geometry of the probe must be supported
    assert geometry_type in ['linear', 'convex', 'matricial'], \
        "Unknown geometry type, please pick either 'linear', 'convex' or " \
        "'matricial'."

    if geometry_type == 'matricial':
        nb_elements = json.loads(config.get('Geometry', 'nb_elements'))
        pitches = json.loads(config.get('Geometry', 'pitch'))
        empty_lines = json.loads(config.get('Geometry', 'empty_lines'))
        nb_elements = list(map(int, nb_elements))
        pitch = list(pitches)
        empty_lines = list(map(int, empty_lines))
    else:
        nb_elements = config.getint('Geometry', 'nb_elements')
        pitch = config.getfloat('Geometry', 'pitch')
        empty_lines = None

    config_dict = {
        'name': config.get('General', 'name'),
        'nb_elements': nb_elements,
        'pitch': pitch,
        'radius': config.getfloat('Geometry', 'radius', fallback=None),
        'empty_lines': empty_lines,
        'central_freq': config.getfloat('Transmission', 'central_freq'),
        'bandwidth': config.getfloat('Transmission', 'bandwidth'),
    }

    return {
        'linear': LinearProbe,
        'convex': ConvexProbe,
        'matricial': MatricialProbe,
    }[geometry_type](config_dict)


def build_probe(geometry_type, nb_elements, pitch, central_freq,
                bandwidth=None, radius=None, empty_lines=None):
    """Builds a probe based on its characteristics, is used when we load data
    from a file with unknown probe name. Not so clean tho.

    :ivar str geometry_type: The type of the probe (either linear, convex or
        matricial). Is defined by child
    :ivar int, list nb_elements: The total number of piezo-electric elements in
        the probe, 2D if matricial
    :ivar float, list pitch: The space, in m, between two piezo-electric
        components, 2D if matricial
    :ivar float central_freq: The central frequency of the probe, in Hz
    :ivar float bandwidth: The bandwidth of the probe (should be between 0 and
        200%), in %
    :ivar float radius: The radius of the curvature, in m
    :ivar list empty_lines: The steps for the matricial empty lines, 2D

    :returns: The Probe class with the main info (central freq, coordinates of
        elements, etc)
    :return type: LinearProbe, ConvexProbe, MatricialProbe
    """
    config_dict = {
        'nb_elements': nb_elements,
        'pitch': pitch,
        'radius': radius,
        'empty_lines': empty_lines,
        'central_freq': central_freq,
        'bandwidth': bandwidth,
    }

    return {
        'linear': LinearProbe,
        'convex': ConvexProbe,
        'matricial': MatricialProbe,
    }[geometry_type](config_dict)


def build_probe_from_geometry(x, y, z, central_freq, bandwidth=None):
    """Builds a probe based on its geometry. Not so clean tho.

    :ivar numpy.ndarray x: The elements positions along the lateral axis (in m)
    :ivar numpy.ndarray y: The elements positions along the elevational axis
        (in m)
    :ivar numpy.ndarray z: The elements positions along the axial axis (in m)
    :ivar float central_freq: The central frequency of the probe, in Hz
    :ivar float bandwidth: The bandwidth of the probe (should be between 0 and
        200%), in %

    :returns: The Probe class with the main info (central freq, coordinates of
        elements, etc)
    :return type: LinearProbe, ConvexProbe, MatricialProbe
    """
    assert x.size == y.size == z.size, \
        "All dimensions should have the same size."

    geometry_type = 'linear'
    if y.any():
        geometry_type = 'matricial'
    elif z.any():
        geometry_type = 'convex'

    config_dict = {
        'nb_elements': x.size,
        'central_freq': central_freq,
        'bandwidth': bandwidth,
        'x': x,
        'y': y,
        'z': z,
    }

    return {
        'linear': LinearProbe,
        'convex': ConvexProbe,
        'matricial': MatricialProbe,
    }[geometry_type](config_dict)
