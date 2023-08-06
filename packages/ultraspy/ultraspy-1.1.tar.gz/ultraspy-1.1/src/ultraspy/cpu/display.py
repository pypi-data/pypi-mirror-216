"""Methods for displaying our beamformed data. These are very straightforward,
so we don't test them.
"""
import numpy as np
import scipy.fftpack
from matplotlib.colors import ListedColormap

from . import normalize


def to_b_mode(data, ref_value=None, safe_zeros=True):
    """Computes the B-Mode of our beamformed data (should have extracted the
    envelope first). Simply returns 20 * log10(data).

    :param numpy.ndarray data: The envelope of our data
    :param float ref_value: A reference value for normalization, if set, the
        normalization will be done using the reference value
    :param bool safe_zeros: If set to True, will replace the zeros values to an
        epsilon to make sure the log10 won't fail

    :returns: The B-Mode
    :return type: numpy.ndarray
    """
    if not np.issubdtype(data.dtype, np.floating):
        raise TypeError(
            f"The data should be of float type, did you extract the envelope "
            f"after beamforming?")

    # Normalize
    data = normalize(data, ref_value)

    if safe_zeros:
        data[data == 0] = np.finfo(float).eps

    return 20 * np.log10(data)


def get_spectrum(data, sampling_freq, average=False, padding=0):
    """Returns the spectrum of a data signal.

    :param numpy.ndarray data: The signal (FFT will be performed on last
        dimension)
    :param float sampling_freq: The sampling frequency of the signal (in Hz)
    :param bool average: If set to True, average the spectra of all the elements
    :param int padding: The number of 0 time samples to pad if the data is not
        long enough

    :returns: The frequencies and their respective distribution
    :return type: tuple
    """
    def reorder(sig):
        half = sig.shape[-1] // 2
        if sig.shape[-1] % 2 == 1:
            half += 1
        return np.concatenate([sig[..., half:], sig[..., :half]], axis=-1)

    # Pads the data if the format is too small
    pads = [(0, 0)] * (data.ndim - 1) + [(0, padding)]
    data_to_fft = np.pad(data, pads, constant_values=0)

    # Get the frequencies distribution and their values
    nb_ts = data_to_fft.shape[-1]
    frequencies = scipy.fftpack.fftfreq(nb_ts) * sampling_freq
    y = np.abs(scipy.fftpack.fft(data_to_fft))

    # If we need to average over a set of data
    if average:
        while y.ndim > 1:
            y = np.mean(y, axis=0)

    # Normalize and returns as dB
    eps = 1e-10
    normed = np.divide(y, np.max(y), out=np.zeros_like(y), where=np.max(y) != 0)
    y = 20 * np.log10(normed, out=np.ones_like(normed) * eps, where=normed != 0)
    return reorder(frequencies), reorder(y)
