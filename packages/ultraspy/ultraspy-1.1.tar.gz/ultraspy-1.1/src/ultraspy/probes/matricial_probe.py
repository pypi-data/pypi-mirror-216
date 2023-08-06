"""Matricial probe class, to store the physical localisation of a matricial
probe elements.
"""
import numpy as np

from .probe import Probe


class MatricialProbe(Probe):
    """MatricialProbe class to handle the matricial probes parameters.

    :ivar str name: The name of the probe
    :ivar str geometry_type: The type of the probe, linear here
    :ivar float central_freq: The central frequency of the probe (in Hz)
    :ivar float bandwidth: The bandwidth of the probe (should be between 0 and
        200%), in %
    :ivar numpy.ndarray geometry: The coordinates of the elements of the probe
    :ivar int nb_elements: The number elements
    """

    def __init__(self, config):
        """Parent initializer, then read the config info to generate the
        matricial geometry.

        :param dict config: The dictionary with the central_freq, the
            nb_elements and, either the x/y/z coordinates, or the pitch and
            empty_lines distribution
        """
        super().__init__(config)
        self._geometry_type = 'matricial'

        # If the geometry has been given, use it
        if all(dim in config for dim in ['x', 'y', 'z']):
            self._geometry[0, :] = config['x']
            self._geometry[1, :] = config['y']
            self._geometry[2, :] = config['z']

        # Else case, we should build a matricial array
        else:
            nx, ny = config['nb_elements']
            ex, ey = config['empty_lines']
            gap_x = 0
            gap_y = 0
            if ex > 0:
                gap_x = nx // ex - (1 if nx // ex == nx / ex else 0)
            if ey > 0:
                gap_y = ny // ey - (1 if ny // ey == ny / ey else 0)
            real_x = nx + gap_x
            real_y = ny + gap_y
            pitch_x, pitch_y = config['pitch']
            xnbs = (np.arange(real_x) - ((real_x - 1) / 2)) * pitch_x
            ynbs = (np.arange(real_y) - ((real_y - 1) / 2)) * pitch_y
            empty_x = [ex * (i + 1) + i for i in range(gap_x)]
            empty_y = [ey * (i + 1) + i for i in range(gap_y)]
            xnbs = np.delete(xnbs, empty_x)
            ynbs = np.delete(ynbs, empty_y)
            xx, yy = np.meshgrid(xnbs, ynbs)
            self._geometry[0, :] = xx.flatten()
            self._geometry[1, :] = yy.flatten()
