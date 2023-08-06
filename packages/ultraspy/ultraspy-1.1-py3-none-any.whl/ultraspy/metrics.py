"""Methods to evaluate the quality of our signals, few metrics.
"""
import logging
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

from .helpers.metrics_helpers import (show_signal_and_noise,
                                      show_beamformed_metrics)
from .utils.masks import create_circular_mask, create_rectangular_mask


logger = logging.getLogger(__name__)


def get_most_salient_point(data, ignore_until=0, show=False):
    """Returns the position which received the highest amplitude.

    :param numpy.ndarray data: The data to evaluate (multidimensional)
    :param int ignore_until: Ignore the first x time samples (assumed to be the
        last axis)
    :param bool show: If set to True, shows the results with matplotlib

    :returns: The indices of the most salient pixel in the image
    :return type: tuple
    """
    ignored = data[..., ignore_until:]
    indices = np.unravel_index(ignored.argmax(), ignored.shape)
    indices = (*indices[:-1], indices[-1] + ignore_until)
    if show:
        data = data.reshape((-1, data.shape[-1]))
        raveled = np.ravel_multi_index(indices[:-1])
        plt.imshow(data, aspect='auto')
        plt.axhline(raveled, data.shape[:-1], color='r')
        plt.axvline(indices[-1], color='r')
        plt.show()
    return indices


def find_signal_and_noise(data, signal_width=20, noise_offset=50,
                          ignore_until=0, noise_size=None, show=False):
    """Returns an estimation of where the signal and noise could be in a signal
    based on its maximum value and some ad-hoc values.

    :param numpy.ndarray data: The sample of data to evaluate (must be 1D)
    :param int, list signal_width: The width of the signal in the data, it can
        be either an integer (total width, centered around maximum value), or a
        list with two integers [nb_time_samples before / after max value].
    :param int noise_offset: The number of time sample to skip between signal
        and noise.
    :param int ignore_until: The number of time sample to ignore at the
        beginning of the data (artificial 0 values at the beginning after
        truncation for example).
    :param int noise_size: The maximum number of time samples for noise. If
        None, takes everything it can.
    :param bool show: If set to True, shows the results with matplotlib

    :returns: The indices of both the signal and the noise
    :return type: tuple
    """
    if isinstance(signal_width, int):
        signal_width = [signal_width // 2, signal_width - (signal_width // 2)]

    # First non-zero element if signal has been truncated:
    noise_ignore_until = max(ignore_until, np.argwhere(data != 0)[0, 0])
    signal_ignore_until = noise_ignore_until + noise_offset + 1

    # Find signal location
    idx_max = np.argmax(data[signal_ignore_until:]) + signal_ignore_until
    signal_x1 = max(signal_ignore_until, idx_max - signal_width[0])
    signal_x2 = min(idx_max + signal_width[1], len(data) - 1)

    # Find noise location
    noise_x1 = noise_ignore_until
    noise_x2 = max(noise_x1, signal_x1 - noise_offset)
    if noise_size is not None:
        noise_x1 = max(noise_x1, noise_x2 - noise_size)

    # Signal / Noise
    signal_sample = data[signal_x1:signal_x2]
    noise_sample = data[noise_x1:noise_x2]

    # Show if requested
    if show:
        show_signal_and_noise(data, signal_sample, noise_sample,
                              (signal_x1, signal_x2), (noise_x1, noise_x2))

    return [signal_x1, signal_x2], [noise_x1, noise_x2]


def signal_noise_ratio(data, signal_bounds, noise_bounds,
                       center=True, max_power=False, show=False):
    """Returns the Signal to Noise ratio of the sample, based on the location
    of both the pulse and the noise.

    .. math::
        SNR = 10 . \\log_{10} \\left ( \\frac{\\sum^{N_{s}} (s^{2} / N_{s})} \
                                             {\\sum^{N_{n}} (n^{2} / N_{n})} \
                              \\right )

    :param numpy.ndarray data: The sample of data to evaluate
    :param tuple signal_bounds: The indices of the signal (pulse) to observe
    :param tuple noise_bounds: The indices of the noise to compare
    :param bool center: If set to True, will center the average of the pulse
        and the noise to 0
    :param bool max_power: If set to True, will take the maximum value of the
        pulse sample only. Else case, it performs an average of the results
    :param bool show: If set to True, shows the results with matplotlib

    :returns: The Signal to Noise Ratio (in dB)
    :return type: float
    """
    # Signal / Noise
    signal_sample = data[signal_bounds[0]:signal_bounds[1]]
    noise_sample = data[noise_bounds[0]:noise_bounds[1]]

    # Show if requested
    if show:
        show_signal_and_noise(data, signal_sample, noise_sample,
                              signal_bounds, noise_bounds)

    if center:
        signal_sample = signal_sample - np.mean(signal_sample)
        noise_sample = noise_sample - np.mean(noise_sample)

    if max_power:
        power_signal = np.square(np.max(np.abs(signal_sample)))
        noise_std = np.square(np.std(noise_sample)) + 1e-10
        return 10 * np.log10(power_signal / noise_std)
    else:
        power_signal = np.mean(np.square(signal_sample))
        power_noise = np.mean(np.square(noise_sample)) + 1e-10
        return 10 * np.log10(power_signal / power_noise)


def get_full_width_at_half_maximum(signal, focus_idx, line_axis, half=-6,
                                   local=True, get_details=False, show=False):
    """Returns the Full-Width at Half Maximum of a signal, given a focus index.
    It is basically the width of the focused lobe at -6dB.

    TODO: It'd be easier to always return the details

    :param numpy.ndarray signal: The sample of data to evaluate
    :param int focus_idx: The index to focus on, we'll look for the lobe around
        this index
    :param numpy.ndarray line_axis: The spatial axis to know the location of
        each pixel
    :param int half: Where to cut the lobe (default to -6dB)
    :param bool local: If set to True, consider local maximum (FWHM is bound to
        maximum of the lobe - half). Else case, arbitrary -6dB is used (or half
        if specified)
    :param bool get_details: If set to True, the function will return the
        details of the computation, which is useful for visualization
    :param bool show: If set to True, shows the results with matplotlib

    :returns: Either the FWHM itself, or a dictionary with the details of the
        computation
    :return type: dict, float
    """
    def lin_interp(xx, yy, i, h):
        return xx[i] + (xx[i+1] - xx[i]) * ((h - yy[i]) / (yy[i+1] - yy[i]))

    if local:
        maximas = scipy.signal.argrelextrema(signal, np.greater)[0]
        local_max = signal[maximas[np.argmin(abs(maximas - focus_idx))]]
        half += local_max
    signs = np.sign(np.add(signal, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    indices = np.where(zero_crossings)[0]

    # Only valid if we have two crossings around our focus point
    idx = 0
    centered = indices - focus_idx
    if (centered <= 0).any() and (centered >= 0).any() and centered.size > 1:
        if centered.size > 2:
            idx = np.argmax(np.where(centered <= 0))
        if idx == indices.size - 1:
            idx -= 1
        fwhm = [lin_interp(line_axis, signal, indices[idx], half),
                lin_interp(line_axis, signal, indices[idx + 1], half)]
    else:
        logger.warning('Did not find half maximum around focus point.')
        return {'fwhm': None, 'lower': None, 'higher': None}

    if show:
        fwhm_info = {'lower': fwhm[0], 'higher': fwhm[1]}
        show_beamformed_metrics(signal, line_axis, focus_idx, fwhm=fwhm_info)

    if get_details:
        return {'fwhm': fwhm[1] - fwhm[0], 'lower': fwhm[0], 'higher': fwhm[1]}
    else:
        return fwhm[1] - fwhm[0]


def get_peak_side_lobe(signal, focus_idx, line_axis, get_details=False,
                       show=False):
    """Returns the Peak Side Lobe of a signal, given a focus index. It is
    basically the difference in dB between the focused lobe and its closest
    neighbor.

    TODO: It'd be easier to always return the details

    :param numpy.ndarray signal: The sample of data to evaluate
    :param int focus_idx: The index to focus on, we'll look for the lobe around
        this index
    :param numpy.ndarray line_axis: The spatial axis to know the location of
        each pixel
    :param bool get_details: If set to True, the function will return the
        details of the computation, which is useful for visualization
    :param bool show: If set to True, shows the results with matplotlib

    :returns: Either the PSL itself, or a dictionary with the details of the
        computation
    :return type: dict, float
    """
    peaks, _ = scipy.signal.find_peaks(signal, prominence=1)
    if peaks.size == 0:
        logger.warning("Flat signal, no peak to observe, can't determine FWHM.")
        return None

    focus_peak_idx = np.argmin(np.abs(peaks - focus_idx))
    before = after = -60
    if focus_peak_idx > 0:
        before = signal[peaks[focus_peak_idx - 1]]
    if focus_peak_idx < peaks.size - 1:
        after = signal[peaks[focus_peak_idx + 1]]

    psl = -max(before, after)
    idx_closest = focus_peak_idx - 1 if before > after else focus_peak_idx + 1

    if show:
        psl_info = {'peaks': peaks, 'closest': idx_closest}
        show_beamformed_metrics(signal, line_axis, focus_idx, psl=psl_info)

    if get_details:
        return {'psl': psl, 'peaks': peaks, 'closest': idx_closest}
    else:
        return psl


def get_lobe_metrics(b_mode, focus, x, z, show=False):
    """Calls both peak side lobe and FWHM methods to return the results in both
    axial and lateral axes.

    :param numpy.ndarray b_mode: The B-Mode image to study (of
        shape (nb_x, nb_z))
    :param tuple focus: The indices to focus on, we'll look for the lobe around
        this position
    :param numpy.ndarray x: The lateral axis
    :param numpy.ndarray z: The axial axis
    :param bool show: If set to True, shows the results with matplotlib

    :returns: A dictionary with the results of both PSL and FWHM computation
        for both lateral and axial axes
    :return type: dict
    """
    # Lateral
    lat_fwhm = get_full_width_at_half_maximum(
        b_mode[:, focus[1]], focus[0], x, get_details=True)
    lat_psl = get_peak_side_lobe(
        b_mode[:, focus[1]], focus[0], x, get_details=True)
    # Axial
    axi_fwhm = get_full_width_at_half_maximum(
        b_mode[focus[0], :], focus[1], z, get_details=True)
    axi_psl = get_peak_side_lobe(
        b_mode[focus[0], :], focus[1], z, get_details=True)

    metrics = {
        'lateral_fwhm': lat_fwhm['fwhm'],
        'lateral_psl': lat_psl['psl'],
        'axial_fwhm': axi_fwhm['fwhm'],
        'axial_psl': axi_psl['psl'],
    }

    if show:
        show_beamformed_metrics(b_mode[:, focus[1]], x, focus[0],
                                fwhm=lat_fwhm, psl=lat_psl, title='Lateral')
        show_beamformed_metrics(b_mode[focus[0], :], z, focus[1],
                                fwhm=axi_fwhm, psl=axi_psl, title='Axial')

    return metrics


def build_mask(position, dimension, x_axis, z_axis, shape='circle'):
    """Build a mask given a numpy area, the shape of the mask and its dimension
    and location. The resulting array is of type bool, with False values within
    the requested shape and True elsewhere. Few shapes are supported:

        - circle: build a circle mask, centered at 'position' with the radius
          'dimension'
        - empty_circle: build an empty circle mask, centered at 'position'. It
          expects 'dimension' to be a tuple with (radius, radius_offset), both
          in m, with radius_offset the width of the circle border
        - rectangle: build a rectangular mask, centered at 'position'. It
          expects 'dimension' to be a tuple with (width, height), both in m
        - square: build a square mask, centered at 'position' with a width of
          'dimension', in m

    :param tuple position: The position of the mask to apply (in m). It is
        either the center of the shape (in case of circle / empty circle), or
        the top left position for square or rectangular masks
    :param float, tuple dimension: The dimension of the shape (check the detail
        of each shape to know what is expected here)
    :param numpy.ndarray x_axis: The lateral axis
    :param numpy.ndarray z_axis: The axial axis
    :param str shape: The requested shape for the mask (can be either 'circle',
        'empty_circle', 'rectangle', 'square')

    :returns: The masked array with the requested mask, it can be used using
        np.ma.masked_where(this_mask, data)
    :return type: numpy.ndarray
    """
    if shape not in ['circle', 'empty_circle', 'rectangle', 'square']:
        raise AttributeError('Unknown shape for mask.')

    # Check the dimensions
    error_msg = "Invalid dimension for shape {}".format(shape)
    if shape in ['circle', 'square']:
        if isinstance(dimension, float) or isinstance(dimension, int):
            dimension = [dimension, dimension]
        elif isinstance(dimension, tuple) and len(dimension) == 2:
            dimension = (dimension[0], dimension[0])
        else:
            assert dimension[0] == dimension[1], error_msg
    else:
        assert isinstance(dimension, tuple), error_msg

    if shape == 'circle':
        mask = create_circular_mask(position, dimension[0], x_axis, z_axis)
    elif shape == 'empty_circle':
        radius, offset = dimension
        mask = create_circular_mask(position, radius, x_axis, z_axis)
        mask_empty = create_circular_mask(position, radius - offset,
                                          x_axis, z_axis)
        mask = mask | ~mask_empty
    else:
        top_left = tuple([position[i] - (dimension[i] / 2) for i in range(2)])
        mask = create_rectangular_mask(top_left, dimension, x_axis, z_axis)

    return mask


def get_contrat_noise_ratio(b_mode, focus_mask, noise_mask, cr=False):
    """Returns the Contrast to Noise ratio of the data, using two masks, one
    for the position of the signal, the other one for the noise.

    .. math::
        CNR = 20 . \\log_{10} \
              \\left ( \\frac{|\\mu_{cyst} - \\mu_{speckle}|} \
                             {{\\sqrt{(\\sigma_{cyst}^{2} + \
                               \\sigma_{speckle}^{2}) / 2}}} \
              \\right )

    Or, if you set cr to True:

    .. math::
        CR = 20 . \\log_{10} \\left ( \\frac{\\mu_{speckle}}{\\mu_{cyst}} \
                             \\right )

    :param numpy.ndarray b_mode: The b_mode to evaluate
    :param numpy.ndarray focus_mask: The mask area where to find the signal
    :param numpy.ndarray noise_mask: The mask area where to find the noise
    :param bool cr: If set to True, will compute the CR instead

    :returns: The Contrast to Noise Ratio (in dB)
    :return type: float
    """
    focus = b_mode[~focus_mask]
    noise = b_mode[~noise_mask]
    if focus.size == 0 or noise.size == 0:
        return 0

    if cr:
        num_ratio = np.mean(noise)
        den_ratio = np.mean(focus)
    else:
        num_ratio = np.abs(np.mean(focus) - np.mean(noise))
        den_ratio = np.sqrt((np.std(focus) ** 2 + np.std(noise) ** 2) / 2)

    return 20 * np.log10(num_ratio / den_ratio)
