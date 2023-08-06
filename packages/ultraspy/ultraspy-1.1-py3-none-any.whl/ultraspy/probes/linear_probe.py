"""Linear Probe class, to compute the physical localisation of a linear probe
elements.
"""
import numpy as np

from .probe import Probe


class LinearProbe(Probe):
    """LinearProbe class to handle the linear probes parameters.

    :ivar str name: The name of the probe
    :ivar str geometry_type: The type of the probe, linear here
    :ivar float central_freq: The central frequency of the probe (in Hz)
    :ivar float bandwidth: The bandwidth of the probe (should be between 0 and
        200%), in %
    :ivar numpy.ndarray geometry: The coordinates of the elements of the probe
    :ivar int nb_elements: The number elements
    """

    def __init__(self, config):
        """Parent initializer, then read the config info to generate the linear
        geometry.

        :param dict config: The dictionary with the central_freq, the
            nb_elements and, either the x/y/z coordinates, or the pitch
        """
        super().__init__(config)
        self._geometry_type = 'linear'

        # If the geometry has been given, use it
        if all(dim in config for dim in ['x', 'y', 'z']):
            self._geometry[0, :] = config['x']
            self._geometry[1, :] = config['y']
            self._geometry[2, :] = config['z']

        # Else case, we should build a linear array with a space based on pitch
        else:
            pitch = config['pitch']
            half = (self.nb_elements - 1) / 2
            xnbs = np.arange(self.nb_elements) - half
            self._geometry[0, :] = xnbs * pitch
