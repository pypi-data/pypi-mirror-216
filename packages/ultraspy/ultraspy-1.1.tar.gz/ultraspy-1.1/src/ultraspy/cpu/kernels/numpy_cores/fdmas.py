"""FDMAS algorithm using numpy.
"""
import numpy as np

from .aperture_ratio import get_aperture_ratio
from .probe_distances import get_distances
from .interpolation import interpolate
from ultraspy.utils.beamformers import get_axes_to_reduce


def combine_bb_dmas(focused_data, axes, to_mean):
    """Combine I/Q signals using method of Shen et al., 2019, basically
    computing the sum of the root-squared moduli, with preserved phase, then
    restore the dimensionality by squaring the resulting sum (or mean if
    requested).

    :param numpy.ma.masked_array focused_data: The focused data for each pixel,
        of shape (nb_t, nb_e, np_p)
    :param tuple axes: The axes to consider when compounding the beamforming
        data
    :param bool to_mean: If True, will average the results

    :returns: Beamformed grid of shape (nb_p,), eventually with the
        transmissions preserved if requested, then (nb_t, nb_p)
    :return type: numpy.array
    """
    phased_sign = np.exp(1j * np.angle(focused_data))
    grid = np.sum(np.sqrt(np.abs(focused_data)) * phased_sign, axis=axes)
    if to_mean:
        grid /= np.sum(~focused_data.mask, axis=axes).astype(grid.dtype)
    return grid ** 2


def combine_dmas(focused_data, axes, to_mean):
    """Combine RF signals using method of Matrone et al., 2014. It is summing
    all the possible combinations of root-squared delays, with preserved signs,
    then dividing by the number of combinations if average mode.

    :param numpy.ma.masked_array focused_data: The focused data for each pixel,
        of shape (nb_t, nb_e, np_p)
    :param tuple axes: The axes to consider when compounding / reduce the
        beamforming data
    :param bool to_mean: If True, will average the results

    :returns: Beamformed grid of shape (nb_p,), eventually with the
        transmissions preserved if requested, then (nb_t, nb_p)
    :return type: numpy.array
    """
    sij = focused_data[:, 0:1, ...] * focused_data[:, 1:, ...]
    val = np.sign(sij) * np.sqrt(np.abs(sij))
    grid = np.sum(val.filled(0), axis=axes)

    for i in range(1, focused_data.shape[1] - 1):
        sij = focused_data[:, i:i+1, ...] * focused_data[:, (i+1):, ...]
        val = np.sign(sij) * np.sqrt(np.abs(sij))
        grid += np.sum(val.filled(0), axis=axes)

    if to_mean:
        c = np.sum(~focused_data.mask, axis=axes).astype(grid.dtype)
        grid /= (c ** 2 + c) / 2

    return grid


def delay_multiply_and_sum(data, is_iq, emitted_probe, received_probe,
                           emitted_thetas, received_thetas, delays,
                           sampling_freq, central_freq, t0,
                           sound_speed, f_number, xs, ys, zs,
                           interpolation_method, reduction_method,
                           emitted_aperture, reduce, compound, is_same_probe):
    """Core code computing the Delay Multiply And Sum algorithm using Numpy
    (in a matricial way). The algorithm:

        - computes the distances between the pixels to beamform and the probe,
          and also the distance in the meridional plane
        - computes the ratios, to know if a pixel is in the sight of a probe
          element. Pixels that are not visible are masked
        - computes the transmissions distances, as the closest probe element to
          each pixel
        - convert into delays, then get the related data using interpolation
        - if needed, perform a phase rotation (for I/Qs)
        - reduce along the selected axes (transmissions or elements), given the
          option modes
        - combines the delays over the elements using either the FDMAS
          algorithm (on RFs) or the BB DMAS algorithm (on I/Q)

    :param numpy.ndarray data: The RFs or I/Qs to beamform, of shape (nb_t,
        nb_re, nb_ts)
    :param bool is_iq: If True, the data are I/Qs. RFs else case
    :param numpy.ndarray emitted_probe: The positions of the elements of the
        emitted probe, of shape (nb_t, nb_ee)
    :param numpy.ndarray received_probe: The positions of the elements of the
        received probe, of shape (nb_t, nb_re)
    :param numpy.ndarray emitted_thetas: The angles for each element of the
        emitted probe (only relevant to convex probes, none else case), of
        shape (nb_t, nb_ee)
    :param numpy.ndarray received_thetas: The angles for each element of the
        received probe (only relevant to convex probes, none else case), of
        shape (nb_t, nb_re)
    :param numpy.ndarray delays: The delays applied to each transmission, for
        each element, of shape (nb_t, nb_ee)
    :param float sampling_freq: The sampling frequency of the acquisition
    :param float central_freq: The center frequency of the probes used for the
        acquisition
    :param float t0: The initial time of recording
    :param float sound_speed: The speed of sound of the scanned medium
    :param float f_number: The aperture of the probes elements. For any position
        of the medium, (z / f_number)-width elements of the probes may have an
        aperture wide enough to observe at depth z
    :param numpy.ndarray xs: The lateral pixels coordinates, of shape (nb_p,)
    :param numpy.ndarray ys: The elevational pixels coordinates, of shape
        (nb_p,)
    :param numpy.ndarray zs: The axial pixels coordinates, of shape (nb_p,)
    :param int interpolation_method: The interpolation method to use (can be 0
        (no interpolation) or 1 (linear))
    :param int reduction_method: This option defines if we average the results
        after beamforming (by the number of locally concerned elements, check
        f_number for details). If 1, Delay And Mean is performed, else cas,
        Delay And Sum
    :param int emitted_aperture: If set to 1 (True), we apply the aperture
        f-number for emitted elements
    :param int reduce: If set to 1 (True), we reduce the data
    :param int compound: If set to 1 (True), we compound the data
    :param int is_same_probe: If True, the emitted and received probes are the
        same

    :returns: Beamformed grid of shape (nb_p,). If the `compound` option is set
        to False, the transmission dimension is preserved
    :return type: numpy.ndarray
    """
    # Distance of the emitted probe to the grid
    e_dist2x, e_dist2y, e_dists = get_distances(emitted_probe, xs, ys, zs)
    if is_same_probe:
        r_dist2x, r_dist2y, r_dists = e_dist2x, e_dist2y, e_dists
    else:
        r_dist2x, r_dist2y, r_dists = get_distances(received_probe, xs, ys, zs)

    # Conversion to mask
    e_dists = np.ma.masked_array(e_dists)
    r_dists = np.ma.masked_array(r_dists)

    # If the emission also has an aperture, we mask the distances outside it,
    # so they are never used
    if emitted_aperture == 1:
        e_ratio = get_aperture_ratio(
            zs, e_dist2x, e_dist2y, e_dists, emitted_thetas, f_number)
        e_dists.mask = abs(e_ratio) > 1

    # Aperture of the received elements
    r_ratio = get_aperture_ratio(
        zs, r_dist2x, r_dist2y, r_dists, received_thetas, f_number)
    r_dists.mask = abs(r_ratio) > 1

    # Transmission delays
    axes_to_expand = tuple(range(delays.ndim, e_dists.ndim))
    delays = np.expand_dims(delays, axis=axes_to_expand)
    transmission = np.min(delays * sound_speed + e_dists, axis=1)

    # Reception delays
    reception = r_dists

    # Compute the delays and get the data given the chosen interpolation method
    tau = (reception + transmission[:, None]) / sound_speed
    delay = tau - t0
    focused_data = interpolate(data, delay * sampling_freq,
                               interpolation_method)
    focused_data.mask = tau.mask

    # To preserve the relative phases
    if is_iq:
        focused_data *= np.exp(2j * np.pi * central_freq * tau)

    # Define if the dimensions we want to reduce
    axes = get_axes_to_reduce(compound, reduce)

    # FDMAS combinations
    core = combine_bb_dmas if is_iq else combine_dmas
    grid = core(focused_data, axes, reduction_method == 1)

    return grid
