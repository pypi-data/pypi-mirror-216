"""Methods to deal with the signals, filtering, RF2IQs, matched filtering...
"""
import numpy as np
import scipy.fftpack
import scipy.signal


def down_mix(data, central_freq, sampling_freq, t0, axis=-1):
    """Down-mixing operation, performs a phase rotation on our data to move the
    spectrum around 0 Hz (involving the returned signal to be complex). The
    down-mixing is performed along the time axis (last one by default).

    :param numpy.ndarray data: The data on which to perform the down-mixing
        (along the last dimension by default)
    :param float central_freq: The central frequency of the signal (in Hz)
    :param float sampling_freq: The sampling frequency of the signal (in Hz)
    :param float t0: The initial time of the recorded samples (in s)
    :param int axis: The axis to performs the down-mixing on

    :returns: The down-mixed data, it has the same shape as 'data'
    :return type: numpy.ndarray
    """
    nb_time_samples = data.shape[axis]
    t = np.arange(nb_time_samples) / sampling_freq + t0
    phase = np.exp(-2j * np.pi * central_freq * t)
    dims = np.ones(data.ndim, int)
    dims[axis] = -1
    phase = phase.reshape(dims)
    return data * phase


def filtfilt(data, cutoff, sampling_freq, filter_type, order=5, axis=-1):
    """Butterworth filtfilt, directly redirects to the scipy implementation. It
    is here to make it easier to switch between CPU and GPU implementations
    without changing the code syntax.

    :param numpy.ndarray data: The data on which to apply the filter (along
        last dimension by default)
    :param float, numpy.ndarray cutoff: The critical frequency for the filtering
        (in Hz). It can be either a float (same cutoff value for the whole
        data), or a numpy array, where it is expected to have the shape of the
        data (except for the time axis). In the latter case, the filtering
        is performed with a different cutoff frequency for each sample
    :param float sampling_freq: The sampling frequency of the signal (in Hz)
    :param str filter_type: The type of the filter ('low' or 'high')
    :param int order: The order of the filter (default to 5)
    :param int axis: The axis to performs the filtering on, default to last

    :returns: The filtered data
    :return type: numpy.ndarray
    """
    supported = ['low', 'high']
    if filter_type not in supported:
        raise AttributeError(
            f"Unknown filter type '{filter_type}', pick one among {supported}.")

    nyquist_frequency = sampling_freq / 2
    w_n = cutoff / nyquist_frequency

    if w_n <= 0 or w_n >= 1:
        raise ValueError(
            f"The critical frequency should be between 0 and "
            f"{nyquist_frequency}Hz.")

    return _filtfilt_wn(data, w_n, filter_type, order=order, axis=axis)


def rf2iq(data, central_freq, sampling_freq, t0, order=5, bandwidth=100,
          axis=-1):
    """Converts raw RF data signals into I/Qs (In-Phase Quadrature). This
    consists in a down-mixing operation (centering the data spectrum at 0Hz),
    followed by a low-pass filter to remove the (previously) negative
    components.

    :param numpy.ndarray data: The data to convert in I/Qs
    :param float central_freq: The central frequency of the signal (in Hz)
    :param float sampling_freq: The sampling frequency of the data (in Hz)
    :param float t0: The initial time of the recorded samples (in s)
    :param int order: The order of the low-pass filter
    :param float bandwidth: The bandwidth of the probes. Default is set to 100,
        which means that the whole information is supposed to be found between
        f0/2 and 3*f0/2 (or between -f0/2 and f0/2 after I/Q conversion). Thus,
        the low-pass filter is set to (bandwidth x f0) / 2
    :param int axis: The axis to performs the conversion on

    :returns: The I/Qs data, of the same shape as data
    :return type: numpy.ndarray
    """
    # Demodulation
    data = down_mix(data, central_freq, sampling_freq, t0, axis)

    # Low pass filter, half Fc in both positive / negative frequencies
    bandwidth /= 100
    half_central = central_freq * (bandwidth / 2)
    half_central = min(half_central, sampling_freq / 4)
    data = filtfilt(data, half_central, sampling_freq, 'low', order, axis)

    # We removed half the frequencies during filtering, so we need to multiply
    # them back by 2 to preserve the amplitudes
    return data * 2


def matched_filter(data, ref_signal, domain='time'):
    """Applies a matched filter to our data, along the last axis, given a
    reference signal which is supposed to match. Two versions are available:

        - the time mode (default) which works in time domain. It is basically
          a cross-correlation of the data with the reference signal, using a
          zero padding to keep it centered all the time.
        - the spectral mode which works in the spectral domain. It multiplies
          the spectrum of our data by the spectrum of the reversed conjugate of
          our reference signal

    :param numpy.ndarray data: The data on which to apply the filter (along
        last dimension)
    :param numpy.ndarray ref_signal: The reference signal (1D)
    :param str domain: The domain to use ('time' (default) or 'spectral')

    :returns: The compressed data
    :return type: numpy.ndarray
    """
    if domain not in ['time', 'spectral']:
        raise AttributeError(
            "Unknown domain to work on. Please choose 'time' or 'spectral'.")

    # Adapt dimensionality of reference signal
    ref_signal = np.expand_dims(ref_signal, list(range(data.ndim - 1)))

    # Matched filtering using scipy, with a method based on the chosen mode
    method = 'fft' if domain == 'spectral' else 'direct'
    return scipy.signal.correlate(data, ref_signal, 'same', method=method)


def normalize(data, ref_value=None):
    """Simply normalizes a signal to values between -1 and 1.

    :param numpy.ndarray data: The data to normalize
    :param float ref_value: A reference value for normalization, if set, the
        normalization will be done using the reference value

    :returns: The normalized data
    :return type: numpy.ndarray
    """
    if ref_value is None:
        ref_value = np.max(np.abs(data))
    return data / ref_value


def _filtfilt_wn(data, w_n, filter_type, order=5, axis=-1):
    """Filtfilt caller, directly calls the scipy implementation. It is
    expecting to have the normalized critical frequency directly (rather than
    the frequency and sampling rate), which is not so intuitive and shouldn't
    be called, use filtfilt instead.

    :param numpy.ndarray data: The data on which to apply the filter (along
        last dimension by default)
    :param float w_n: The critical frequency (normalized between 0 and 1, with
        1 the nyquist frequency)
    :param str filter_type: The type of the filter ('low' or 'high')
    :param int order: The order of the filter (default to 5)
    :param int axis: The axis to performs the filtering on

    :returns: The filtered data
    :return type: numpy.ndarray
    """
    b, a = scipy.signal.butter(order, w_n, filter_type)
    return scipy.signal.filtfilt(b, a, data, axis=axis)
