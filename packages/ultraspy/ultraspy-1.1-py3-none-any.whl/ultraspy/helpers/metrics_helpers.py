"""Matplotlib visualization helpers for visualization. As everything here is
solely for visualization purposes, it doesn't need to be tested.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from ultraspy.utils.matplot import add_rectangle_patch


def show_signal_and_noise(signal,
                          signal_sample, noise_sample,
                          signal_bounds, noise_bounds):
    """Shows the data signal and highlights both the signal and noise.

    :param numpy.ndarray signal: The signal to plot
    :param numpy.ndarray signal_sample: The signal sample (might have been
        preprocessed so could be different from the signal)
    :param numpy.ndarray noise_sample: The noise sample (might have been
        preprocessed so could be different from the signal)
    :param tuple signal_bounds: The boundaries for the signal (left and right
        indices)
    :param tuple noise_bounds: The boundaries for the noise (left and right
        indices)
    """
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 2)
    ax = fig.add_subplot(gs[0, :])
    ax.plot(signal)
    ax.set_xlabel('Time samples')
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    add_rectangle_patch(ax, signal_sample, signal_bounds, 'Signal')
    add_rectangle_patch(ax, noise_sample, noise_bounds, 'Noise')

    ax = fig.add_subplot(gs[1, 0])
    ax.plot(np.arange(*noise_bounds), noise_sample)
    ax.set_title('Noise')
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(np.arange(*signal_bounds), signal_sample)
    ax.set_title('Signal')
    plt.show()


def show_beamformed_metrics(signal, line_axis, focus_idx, fwhm=None, psl=None,
                            focus_offset=60, title=''):
    """Shows the metrics of the beamformed data, meaning the PSL and FWHM.

    :param numpy.ndarray signal: The signal to plot
    :param numpy.ndarray line_axis: The spatial axis of the data
    :param int focus_idx: The index of the FWHM to find (and PSL to draw right
        next to the peak)
    :param dict fwhm: The dictionary info about the fwmh, expects lower and
        higher, the positions of the lobe at -6dB. If None, the FWHM is not
        displayed
    :param dict psl: The dictionary info about the psl, expects peaks, the
        position of all the peaks in the set of data and closest, the index of
        the closest peak
    :param int focus_offset: The number of time samples to display around the
        focusing point
    :param str title: The title to display
    """
    def show_peak_side_lobe(ax, vals_x, vals_y, peaks, closest):
        ax.plot(vals_x[peaks], vals_y[peaks], 'ob')
        ax.annotate(text='', xy=(vals_x[closest], vals_y[closest]),
                    xytext=(vals_x[closest], 0),
                    arrowprops=dict(arrowstyle='<->'))

    def show_full_width_half_maximum(ax, lower, higher):
        ax.annotate(text='', xy=(lower, -8), xytext=(higher, -8),
                    arrowprops=dict(arrowstyle='<->'))
        ax.text(higher + abs(higher - lower), -5, '-6dB')
        ax.axhline(-6, ls='--')

    i1 = max(0, focus_idx - focus_offset)
    i2 = min(focus_idx + focus_offset, line_axis.size - 1)
    sample = signal[i1:i2]
    sample_axis = line_axis[i1:i2]

    fig, axs = plt.subplots(2)
    axs[0].plot(line_axis, signal)
    axs[0].axvline(line_axis[i1], c='b', ls=':')
    axs[0].axvline(line_axis[i2], c='b', ls=':')
    axs[1].plot(sample_axis, sample)
    if psl is not None:
        p = psl['peaks']
        psl['closest'] = p[psl['closest']] - i1
        psl['peaks'] = p[(p >= i1) & (p < i2)] - i1
        psl.pop('psl', None)
        show_peak_side_lobe(axs[1], sample_axis, sample, **psl)
    if fwhm is not None:
        fwhm.pop('fwhm', None)
        show_full_width_half_maximum(axs[1], **fwhm)

    axs[0].set_ylim([-60, 0])
    axs[1].set_ylim([-60, 0])
    fig.suptitle(title)
    plt.show()
