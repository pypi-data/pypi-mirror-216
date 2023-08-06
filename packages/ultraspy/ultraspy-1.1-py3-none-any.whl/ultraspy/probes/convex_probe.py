"""Convex probe class, to store the physical localisation of a convex probe
elements.
"""
import numpy as np

from .probe import Probe


class ConvexProbe(Probe):
    """ConvexProbe class to handle the convex probes parameters.

    :ivar str name: The name of the probe
    :ivar str geometry_type: The type of the probe, convex here
    :ivar float central_freq: The central frequency of the probe (in Hz)
    :ivar float bandwidth: The bandwidth of the probe (should be between 0 and
        200%), in %
    :ivar numpy.ndarray geometry: The coordinates of the elements of the probe
    :ivar int nb_elements: The number elements
    :ivar float radius: The radius of the curvature, in m
    :ivar float thetas: The thetas of the probe for each element, in rad
    """

    def __init__(self, config):
        """Parent initializer, then read the config info to generate the convex
        geometry.

        :param dict config: The dictionary with the central_freq, the
            nb_elements, the pitch, and the radius
        """
        super().__init__(config)
        self._geometry_type = 'convex'

        # If the geometry has been given, use it
        if all(dim in config for dim in ['x', 'y', 'z']):
            self._geometry[0, :] = config['x']
            self._geometry[1, :] = config['y']
            self._geometry[2, :] = config['z']
            # TODO: Not done yet, should think about the geometry
            raise NotImplementedError("Should compute radius / thetas from "
                                      "positions of the probe elements.")

        # Else case, we should build a convex array with angles based on the
        # probe radius, then the x / z positions
        else:
            pitch = config['pitch']
            radius = config['radius']
            ra = np.arcsin(pitch / (2 * radius))
            chord = 2 * radius * np.sin(ra * (self.nb_elements - 1))
            min_height = np.sqrt(radius ** 2 - ((chord ** 2) / 4))
            self._thetas = np.linspace(np.arctan2(-chord/2, min_height),
                                       np.arctan2(chord/2, min_height),
                                       self.nb_elements)
            self._geometry[0, :] = radius * np.sin(self._thetas)
            self._geometry[2, :] = radius * np.cos(self._thetas)
            self._geometry[2, :] -= np.min(self.geometry[2, :])

    def get_thetas(self):
        """Overrides the parent method, return the thetas of each probe
        element, they are used for the f-number in beamformers.
        """
        return self._thetas
