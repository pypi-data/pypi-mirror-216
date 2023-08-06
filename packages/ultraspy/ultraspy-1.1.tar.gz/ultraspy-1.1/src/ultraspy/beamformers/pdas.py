"""The p-DAS beamformer running on GPU.
"""
import logging
import numpy as np

from .beamformer import Beamformer
from ultraspy.utils.beamformers import get_axes_to_reduce

from ultraspy.cpu.kernels.numpy_cores import pdas as numpy_pdas
from ultraspy.cpu.kernels.numba_cores import pdas as numba_pdas

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.beamformers_kernels import k_pdas, k_packet_pdas

import ultraspy as us


logger = logging.getLogger(__name__)


class PDelayAndSum(Beamformer):
    """The PDelayAndSum class, inherit from the Beamformer class (which deals
    with the beamforming setups) and performs the beamforming itself. The class
    is working on either Cupy (CUDA, GPU) or Numpy / Numba (CPU) depending on
    the selected mode (check the doc and the ULTRASPY_CPU_LIB environment
    variable for more information).

    :ivar str name: The name of the Beamforming method
    :ivar bool is_iq: If set to True, will perform the beamforming expecting
        I/Qs
    :ivar bool on_gpu: If set to True, will perform the beamforming on GPU
    :ivar bool is_same_probe: If set to True, the emission sequences and the
        reception sequences are the same (mostly standard plane waves),
        else case, both sequences are different (mostly STA)
    :ivar list transmissions_indices: The list of the transmissions indices to
        select
    :ivar dict setup: The characteristics of the beamformer, see the getter to
        have the list of the parameters
    :ivar dict options: The options of the beamformer, see the getter to have
        the list of the parameters
    :ivar numpy.ndarray delays: The delays applied to each element, for each
        transmission, of shape (nb_transmission, nb_emitted_elements)
    :ivar numpy.ndarray emitted_probe: The 3D position of each of the element
        of the emitted probe, per transmission, of shape (nb_transmission,
        nb_emitted_elements)
    :ivar numpy.ndarray received_probe: The 3D position of each of the element
        of the received probe, per transmission, of shape (nb_transmission,
        nb_received_elements)
    :ivar numpy.ndarray emitted_thetas: The thetas of each of the element
        of the emitted probe, per transmission, of shape (nb_transmission,
        nb_emitted_elements). Only used for convex probes
    :ivar numpy.ndarray received_thetas: The 3D position of each of the element
        of the received probe, per transmission, of shape (nb_transmission,
        nb_received_elements). Only used for convex probes
    :param float p: The p factor for non-linear operations in p-DAS
    :param bool use_shen_version: If set to True, the I/Qs version of the
        beamformer will be the one from Shen et al. (BB p-DMAS), which
        causes a phase_shift, leading to aliasing in Doppler. Else case,
        will perform BB p-DAS to preserve the spectrum at f0 (Ecarlat et
        al., 2022)
    """

    def __init__(self, is_iq=False, on_gpu=True, p=2, use_shen_version=False):
        """Initializes the Beamformer parent first, then set the options for
        p-DAS.

        :param bool is_iq: If set to True, the beamformer expects to process
            I/Qs data
        :param bool on_gpu: If True, all the setups are defined on GPU
        :param float p: The p factor for non-linear operations in p-DAS
        :param bool use_shen_version: If set to True, the I/Qs version of the
            beamformer will be the one from Shen et al. (BB p-DMAS), which
            causes a phase_shift, leading to aliasing in Doppler. Else case,
            will perform BB p-DAS to preserve the spectrum at f0 (Ecarlat et
            al., 2022)
        """
        super().__init__(is_iq=is_iq, on_gpu=on_gpu)
        self._name = 'pDAS'
        self._p = p
        self._use_shen_version = use_shen_version

    @property
    def p(self):
        """Get the p value.
        """
        return self._p

    @property
    def use_shen_version(self):
        """Get the Shen mode.
        """
        return self._use_shen_version

    def set_p(self, p):
        """Updates the p value.

        :param float p: The new p factor
        """
        self._p = p

    def set_use_shen_version(self, use_shen_version):
        """Updates the baseband mode.

        :param bool use_shen_version: If set to True, use the version of Shen
            et al. (BB p-DMAS)
        """
        self._use_shen_version = use_shen_version

    def beamform_gpu(self, d_data, scan):
        """Runs the p-DAS beamformer using cupy (CUDA kernel on GPU).

        :param cupy.array d_data: The cupy.array data to beamform, stored on
            GPU, either in float or complex, based on the beamforming mode. The
            shape should be (nb_transmissions, nb_emitted_elements,
            nb_time_samples)
        :param Scan scan: The  scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but its last dimensions will be the one requested in
            scan.shape. If compound option is set to False, it will preserve
            the transmissions and look like (nb_transmissions, \\*scan.shape)
        :return type: cupy.array
        """
        # Shortcuts
        ss = self.setups
        so = self.options

        # If the coordinates are on CPU, send them to GPU
        if not scan.on_gpu:
            scan.set_on_gpu(True)

        _, nb_re, nb_ts = d_data.shape
        nb_t, nb_ee = self.delays.shape
        d_xx, d_yy, d_zz = scan.ravel_pixels()
        nb_pixels = d_xx.size
        dim_nb_t = nb_t if so['compound'] == 0 else 1
        dim_nb_re = nb_re if so['reduce'] == 0 else 1
        d_grid = gpu_utils.send_to_gpu(
            np.zeros((dim_nb_t, dim_nb_re, nb_pixels)), np.complex64)
        d_delays = gpu_utils.send_to_gpu(
            np.zeros((nb_pixels, nb_re)), np.complex64)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
        k_pdas(g_dim, b_dim,
               (d_data, np.uint32(self.is_iq),
                self.emitted_probe, self.received_probe,
                self.emitted_thetas, self.received_thetas, self.delays,
                np.uint32(nb_t), np.uint32(nb_ee), np.uint32(nb_re),
                np.uint32(nb_ts),
                ss['sampling_freq'], ss['central_freq'], np.float32(self.t0),
                ss['sound_speed'], ss['f_number'],
                d_xx, d_yy, d_zz,
                np.uint32(dim_nb_t), np.uint32(dim_nb_re),
                d_delays, d_grid, np.uint32(nb_pixels),
                np.float32(self.p), np.uint32(self.use_shen_version),
                so['interpolation'], so['reduction'], so['rx_apodization'],
                so['rx_apodization_alpha'], so['emitted_aperture'],
                so['compound'], so['reduce']))

        axes = get_axes_to_reduce(so['compound'], so['reduce'])
        d_grid = gpu_utils.squeeze_axes(d_grid, axes=axes)
        d_grid = gpu_utils.reshape(d_grid, d_grid.shape[:-1] + scan.shape)

        # If we're working on RFs, we need to bandpass the second harmonics to
        # remove DC
        d_grid = self._filter_second_harmonics(d_grid, scan.axial_step)

        return d_grid

    def beamform_cpu(self, data, scan):
        """Runs the p-DAS beamformer using either Numpy (matricial operations)
        or the no-python iterative mode of Numba (faster).

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param Scan scan: the scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but its last dimensions will be the one requested in
            scan.shape. If compound option is set to False, it will preserve
            the transmissions and look like (nb_transmissions, \\*scan.shape)
        :return type: numpy.ndarray
        """
        # Redirects to the proper method
        is_numpy = cfg.CPU_LIB == 'numpy'
        core = self._beamform_numpy if is_numpy else self._beamform_numba

        # If the coordinates are on GPU, send them back to CPU
        if scan.on_gpu:
            scan.set_on_gpu(False)

        # Calls the beamformer
        xx, yy, zz = scan.ravel_pixels()
        grid = core(data, xx, yy, zz, self.setups, self.options)
        grid = np.reshape(grid, grid.shape[:-1] + scan.shape)

        # If we're working on RFs, we need to bandpass the second harmonics to
        # remove DC
        grid = self._filter_second_harmonics(grid, scan.axial_step)

        return grid

    def beamform_packet_gpu(self, d_data, scan):
        """Runs the p-DAS beamformer on a packet of data using cupy (CUDA
        kernel on GPU).

        :param cupy.array d_data: The cupy.array data to beamform, stored on
            GPU, either in float or complex, based on the beamforming mode. The
            shape should be (nb_frames, nb_transmissions, nb_emitted_elements,
            nb_time_samples)
        :param Scan scan: The  scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but if compound and reduce are set to True, its shape
            would be (\\*scan.shape, nb_frames). If reduce or compound are set
            to False, their respective dimensions will be preserved in the first
            dimensions as for the ::code::`beamform` method above
        :return type: cupy.array
        """
        # Shortcuts
        ss = self.setups
        so = self.options

        # If the coordinates are on CPU, send them to GPU
        if not scan.on_gpu:
            scan.set_on_gpu(True)

        nb_f, _, nb_re, nb_ts = d_data.shape
        nb_t, nb_ee = self.delays.shape
        d_xx, d_yy, d_zz = scan.ravel_pixels()
        nb_pixels = d_xx.size
        dim_nb_t = nb_t if so['compound'] == 0 else 1
        dim_nb_re = nb_re if so['reduce'] == 0 else 1
        d_grid = gpu_utils.send_to_gpu(
            np.zeros((dim_nb_t, dim_nb_re, nb_pixels, nb_f)), np.complex64)
        d_delays = gpu_utils.send_to_gpu(
            np.zeros((nb_pixels, nb_f, nb_re)), np.complex64)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels * nb_f)
        k_packet_pdas(g_dim, b_dim,
                      (d_data, np.uint32(self.is_iq),
                       self.emitted_probe, self.received_probe,
                       self.emitted_thetas, self.received_thetas, self.delays,
                       np.uint32(nb_f), np.uint32(nb_t),
                       np.uint32(nb_ee), np.uint32(nb_re), np.uint32(nb_ts),
                       ss['sampling_freq'], ss['central_freq'],
                       np.float32(self.t0), ss['sound_speed'], ss['f_number'],
                       d_xx, d_yy, d_zz,
                        np.uint32(dim_nb_t), np.uint32(dim_nb_re),
                       d_delays, d_grid, np.uint32(nb_pixels * nb_f),
                       np.float32(self.p), np.uint32(self.use_shen_version),
                       so['interpolation'], so['reduction'],
                       so['rx_apodization'], so['rx_apodization_alpha'],
                       so['emitted_aperture'], so['compound'], so['reduce']))

        axes = get_axes_to_reduce(so['compound'], so['reduce'])
        d_grid = gpu_utils.squeeze_axes(d_grid, axes=axes)
        d_grid = gpu_utils.reshape(
            d_grid, d_grid.shape[:-2] + scan.shape + d_grid.shape[-1:])

        # If we're working on RFs, we need to bandpass the second harmonics to
        # remove DC
        d_grid = self._filter_second_harmonics(d_grid, scan.axial_step, axis=-2)

        return d_grid

    def beamform_packet_cpu(self, data, scan):
        """Runs the p-DAS beamformer on a packet of data using either Numpy
        (matricial operations) or the no-python iterative mode of Numba
        (faster).

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_frames, nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param Scan scan: the scan to beamform, with the pixels we are willing
            to process

        :returns: The beamformed data. Its shape depends on the beamforming
            options, but if compound and reduce are set to True, its shape
            would be (\\*scan.shape, nb_frames). If compound is set to False,
            the transmissions will be preserved in the first dimension as for
            the ::code::`beamform` method above
        :return type: numpy.ndarray
        """
        # If the coordinates are on GPU, send them back to CPU
        if scan.on_gpu:
            scan.set_on_gpu(False)

        # Redirects to the proper method
        is_numpy = cfg.CPU_LIB == 'numpy'
        core = self._beamform_packet_numpy if is_numpy \
            else self._beamform_packet_numba

        # Calls the beamformer
        xx, yy, zz = scan.ravel_pixels()
        grid = core(data, xx, yy, zz, self.setups, self.options)
        grid = np.reshape(grid, grid.shape[:-2] + scan.shape + grid.shape[-1:])

        # If we're working on RFs, we need to bandpass the second harmonics to
        # remove DC
        grid = self._filter_second_harmonics(grid, scan.axial_step, axis=-2)

        return grid

    def _checkup_lib_compatibility(self, option_name, option_value):
        """Checks if the current library used (numpy or numba) is compatible
        with the new selected option.

        :param str option_name: The name of the option to change
        :param int, float option_value: The value to update

        :returns: The new value for the option, that will work for sure
        :return type: int, float
        """
        option_value = super()._checkup_lib_compatibility(
            option_name, option_value)

        # Additional constraint of p-DAS algorithm
        if option_name == 'reduce':
            if option_value == 0:
                logger.warning("Reduction must be done with p-DAS.")
                option_value = 1

        return option_value

    def _filter_second_harmonics(self, beamformed, axial_step, axis=-1):
        """Filters the beamformed array along the last axis around the second
        harmonics.

        :param numpy.ndarray, cupy.array beamformed: the beamformed data
        :param float axial_step: the step in the axial axis used for beamforming
        :param int axis: the axis on which to perform the filtering (the axial
            dimension). By default, the last one

        :returns: The filtered beamformed data without DC
        :return type: numpy.ndarray, cupy.array
        """
        if not self.is_iq:
            delta_axial = (1 / axial_step)
            beamformed_fs = delta_axial * self.setups['sound_speed'] / 2
            beamformed_f0 = self.setups['central_freq']
            fc1 = 0.5 * beamformed_f0
            fc2 = 1.5 * beamformed_f0

            if self.on_gpu:
                us.filtfilt(beamformed, fc1, beamformed_fs, 'high', axis=axis)
                us.filtfilt(beamformed, fc2, beamformed_fs, 'low', axis=axis)
            else:
                beamformed = us.cpu.filtfilt(beamformed, fc1, beamformed_fs,
                                             'high', axis=axis)
                beamformed = us.cpu.filtfilt(beamformed, fc2, beamformed_fs,
                                             'low', axis=axis)

        return beamformed

    ###########################################################################
    # Numpy callers
    ###########################################################################
    def _beamform_numpy(self, data, xs, ys, zs, setups, options):
        """Caller, will call Numpy beamforming kernel.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param numpy.ndarray xs: the lateral coordinates of the pixels, ravelled
        :param numpy.ndarray ys: the elevational coordinates of the pixels,
            ravelled
        :param numpy.ndarray zs: the axial coordinates of the pixels, ravelled
        :param dict setups: the dictionary with the setups info
        :param dict options: the dictionary with the options info

        :returns: The beamformed data, of shape (nb_kept_transmissions,
            nb_kept_elements, nb_pixels)
        :return type: numpy.ndarray
        """
        return numpy_pdas.p_delay_and_sum(
            data, self.is_iq,
            self.emitted_probe, self.received_probe,
            self.emitted_thetas, self.received_thetas, self.delays,
            setups['sampling_freq'], setups['central_freq'],
            np.float32(self.t0), setups['sound_speed'], setups['f_number'],
            xs, ys, zs,
            self.p, self.use_shen_version,
            options['interpolation'], options['reduction'],
            options['emitted_aperture'], options['reduce'], options['compound'],
            self.is_same_probe)

    def _beamform_packet_numpy(self, data, xs, ys, zs, setups, options):
        """Caller, will call Numpy beamforming kernel on a packet of frames.

        TODO: I think the packet with no compound doesn't work here, this
            should be checked / tested

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_frames, nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param numpy.ndarray xs: the lateral coordinates of the pixels, ravelled
        :param numpy.ndarray ys: the elevational coordinates of the pixels,
            ravelled
        :param numpy.ndarray zs: the axial coordinates of the pixels, ravelled
        :param dict setups: the dictionary with the setups info
        :param dict options: the dictionary with the options info

        :returns: The beamformed data, of shape (nb_kept_transmissions,
            nb_kept_elements, nb_pixels, nb_frames)
        :return type: numpy.ndarray
        """
        packet_size = data.shape[0]
        packet = np.zeros((xs.size, packet_size), dtype=data.dtype)
        for f in range(packet_size):
            packet[..., f] = self._beamform_numpy(data[f], xs, ys, zs,
                                                  setups, options)
        return packet

    ###########################################################################
    # Numba callers
    ###########################################################################
    def _beamform_numba(self, data, xs, ys, zs, setups, options):
        """Caller, will call Numba beamforming kernel.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param numpy.ndarray xs: the lateral coordinates of the pixels, ravelled
        :param numpy.ndarray ys: the elevational coordinates of the pixels,
            ravelled
        :param numpy.ndarray zs: the axial coordinates of the pixels, ravelled
        :param dict setups: the dictionary with the setups info
        :param dict options: the dictionary with the options info

        :returns: The beamformed data, of shape (nb_kept_transmissions,
            nb_kept_elements, nb_pixels)
        :return type: numpy.ndarray
        """
        grid = numba_pdas.p_delay_and_sum(
            data, self.is_iq,
            self.emitted_probe, self.received_probe,
            self.emitted_thetas, self.received_thetas, self.delays,
            setups['sampling_freq'], setups['central_freq'],
            np.float32(self.t0), setups['sound_speed'], setups['f_number'],
            xs, ys, zs,
            self.p, self.use_shen_version,
            options['interpolation'], options['reduction'],
            options['rx_apodization'], options['rx_apodization_alpha'],
            options['emitted_aperture'], options['reduce'], options['compound'],
            self.is_same_probe)

        if not self.is_iq:
            grid = grid.real

        axes = get_axes_to_reduce(options['compound'], options['reduce'])
        grid = np.squeeze(grid, axis=axes)

        return grid

    def _beamform_packet_numba(self, data, xs, ys, zs, setups, options):
        """Caller, will call Numba beamforming kernel on a packet of frames.

        :param numpy.ndarray data: the data to beamform, either in float or
            complex, based on the beamforming mode. The shape should be
            (nb_frames, nb_transmissions, nb_emitted_elements, nb_time_samples)
        :param numpy.ndarray xs: the lateral coordinates of the pixels, ravelled
        :param numpy.ndarray ys: the elevational coordinates of the pixels,
            ravelled
        :param numpy.ndarray zs: the axial coordinates of the pixels, ravelled
        :param dict setups: the dictionary with the setups info
        :param dict options: the dictionary with the options info

        :returns: The beamformed data, of shape (nb_kept_transmissions,
            nb_kept_elements, nb_pixels, nb_frames)
        :return type: numpy.ndarray
        """
        grid = numba_pdas.p_delay_and_sum_packet(
            data, self.emitted_probe, self.received_probe,
            self.emitted_thetas, self.received_thetas, self.delays,
            setups['sampling_freq'], setups['central_freq'],
            np.float32(self.t0), setups['sound_speed'], setups['f_number'],
            xs, ys, zs,
            self.p, self.use_shen_version,
            options['interpolation'], options['reduction'],
            options['rx_apodization'], options['rx_apodization_alpha'],
            options['emitted_aperture'], options['reduce'], options['compound'],
            self.is_same_probe)

        if not self.is_iq:
            grid = grid.real

        axes = get_axes_to_reduce(options['compound'], options['reduce'])
        grid = np.squeeze(grid, axis=axes)

        return grid
