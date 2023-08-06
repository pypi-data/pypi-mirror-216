"""Methods for displaying our beamformed data.
"""
import numpy as np
from matplotlib.colors import ListedColormap

import ultraspy as us

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.operators_kernels import k_to_db


def to_b_mode(d_data, ref_value=None, inplace=True):
    """Computes the B-Mode of our beamformed data (should have extracted the
    envelope first). Simply returns 20 * log10(data).

    :param cupy.array d_data: The GPUArray data stored on GPU, of dtype float32
        (we’ve extracted the envelope)
    :param float ref_value: A reference value for normalization, if set, the
        normalization will be done using the reference value
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The B-Mode image if inplace is False, else case return None and
        d_data is modified directly
    :return type: cupy.array
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_data.shape, d_data.dtype)
        gpu_utils.set_values(d_new, d_data)
        to_b_mode(d_new, ref_value)
        return d_new

    if d_data.dtype != np.dtype('float32'):
        raise TypeError('The data should be of float type, did you extract '
                        'envelope after beamforming?')

    # Normalize the data
    us.normalize(d_data, ref_value)

    # To Decibel
    g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)
    k_to_db(g_dim, b_dim, (d_data, np.uint32(d_data.size)))


def get_spectrum(d_data, sampling_freq, padding=0):
    """Returns the spectrum of a data signal.

    :param cupy.array d_data: The signal (must be 1D)
    :param float sampling_freq: The sampling frequency of the signal (in Hz)
    :param int padding: The number of 0 time samples to pad if the data is not
        long enough

    :returns: The frequencies and their respective distribution
    :return type: tuple
    """
    raise NotImplementedError("Not implemented on GPU yet, please use the CPU "
                              "version.")


def get_doppler_colormap(use='matplotlib'):
    """Returns a color map proposition for Doppler, based on typical
    echographs, from blue (flow going away from the probe), to red (going
    toward to).

    :param str use: The lib which will use the colormap, either 'matplotlib' or
        'pyqt'

    :returns: The matplotlib map with the RGB value of our color maps
    :return type: matplotlib.colors.ListedMaps
    """
    x = np.linspace(0, 1, 256)
    reds = np.clip(np.sqrt(np.clip(x - 0.5, 0, 1)) * 1.8, 0, 1)
    greens = np.power(x - 0.5, 4) * -8 + np.power(x - 0.5, 2) * 6
    blues = 1.1 * np.sqrt(0.5 - np.clip(x, 0, 0.5))

    if use == 'matplotlib':
        rgb = np.stack((reds, greens, blues, np.ones(256))).T
        return ListedColormap(rgb)
    elif use == 'pyqt':
        rgb = np.stack((reds, greens, blues)).T * 255
        return rgb
    else:
        raise AttributeError(
            f"Unknown library {use}, should pick matplotlib or pyqt.")

