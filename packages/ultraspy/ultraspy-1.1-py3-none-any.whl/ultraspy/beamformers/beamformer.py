"""Beamformer class, to perform the actual beamforming algorithm based on the
data, the scan and everything.
"""
import logging
import numpy as np
import scipy.signal

from . import setups as bf_setups
from . import options as bf_options

from ultraspy.utils.print import dict_to_list_str

from ultraspy.cpu.kernels.numpy_cores.aperture_ratio import get_aperture_ratio
from ultraspy.cpu.kernels.numpy_cores.probe_distances import get_distances

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.operators_kernels import k_get_modulo

import ultraspy as us


logger = logging.getLogger(__name__)


class Beamformer(object):
    """Beamformer class to handle the beamforming parameters.

    :ivar str name: The name of the Beamforming method
    :ivar bool is_iq: If set to True, will perform the beamforming expecting
        I/Qs
    :ivar bool on_gpu: If set to True, will perform the beamforming on GPU
    :ivar bool is_same_probe: If set to True, the emission sequences and the
        reception sequences are the same (mostly standard plane waves),
        else case, both sequences are different (mostly STA)
    :ivar dict setups: The characteristics of the beamformer, see the getter to
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
    """

    def __init__(self, is_iq=False, on_gpu=True):
        """Initialization for the Beamformer. Just initializes both the setups
        and options dictionaries with the default values.

        :param bool is_iq: If True, the beamforming is expecting I/Qs, the
            input data should be RFs else case
        :param bool on_gpu: If True, all the setups are defined on GPU
        """
        self._name = None
        self._is_iq = is_iq
        self._on_gpu = on_gpu
        self._is_same_probe = True
        self.setups = {}
        self.options = {}
        self._initialize_setups()
        self._initialize_options()

    def __str__(self):
        """String sentence to show the beamformer characteristics. Note that it
        is using pretty_print functions, not all data are displayed for ease of
        read.

        :returns: The string sentence to print
        :return type: str
        """
        return '\n'.join([
            '====== Beamformer: ======',
            'name: {}'.format(self.name),
            '(on {}, with {})'.format('I/Qs' if self.is_iq else 'RFs',
                                      'GPU' if self.on_gpu else 'CPU'),
            '\n'.join(dict_to_list_str(self.setups, 2)),
        ])

    @property
    def name(self):
        return self._name

    @property
    def is_iq(self):
        return self._is_iq

    @property
    def on_gpu(self):
        return self._on_gpu

    @property
    def is_same_probe(self):
        return self._is_same_probe

    @property
    def delays(self):
        """Get the delays based on the transmissions to pick.

        :returns: The delays of the sequence
        :return type: numpy.ndarray
        """
        return self.setups['delays'][self.setups['transmissions_idx'], :]

    @property
    def emitted_probe(self):
        """Get the probe used for the emission based on the transmissions to
        pick.

        :returns: The emitted probe elements
        :return type: numpy.ndarray
        """
        return self.setups['emitted_probe'][:, self.setups['transmissions_idx']]

    @property
    def received_probe(self):
        """Get the probe used for the reception based on the transmissions to
        pick.

        :returns: The reception probe elements
        :return type: numpy.ndarray
        """
        ss = self.setups
        return ss['received_probe'][:, ss['transmissions_idx']]

    @property
    def emitted_thetas(self):
        """Get the thetas used for the emission based on the transmissions to
        pick.

        :returns: The emitted thetas elements
        :return type: numpy.ndarray
        """
        ss = self.setups
        return ss['emitted_thetas'][ss['transmissions_idx'], :]

    @property
    def received_thetas(self):
        """Get the thetas used for the reception based on the transmissions to
        pick.

        :returns: The reception thetas elements
        :return type: numpy.ndarray
        """
        ss = self.setups
        return ss['received_thetas'][ss['transmissions_idx'], :]

    @property
    def t0(self):
        """Get the initial time t0, based on the option 'fix_to'. If set to
        True, returns t0 - (sig_duration / 2).

        :returns: The fixed t0 or t0
        :return type: float
        """
        if self.options['fix_t0']:
            return self.setups['t0'] - (self.setups['signal_duration'] / 2)
        else:
            return self.setups['t0']

    def set_is_iq(self, is_iq):
        """Updates the is_iq attribute if requested, useful to process
        beamforming / envelope the proper way.

        :param bool is_iq: True if is I/Q
        """
        self._is_iq = is_iq

    def set_on_gpu(self, on_gpu):
        """Updates the on_gpu attribute if requested, will change the format
        of the setups / options data.

        :param bool on_gpu: True if is on GPU
        """
        if on_gpu and not cfg.GPU_AVAILABLE:
            logging.error('No GPU available on this system, kept CPU mode.')
            return

        for k, v in self.setups.items():
            _, d_type, is_array = bf_setups.INFO[k]
            if is_array:
                # Was on GPU, changes to CPU
                if self.on_gpu and not on_gpu:
                    self.setups[k] = v.get()

                # Was on CPU, switch to GPU
                elif not self.on_gpu and on_gpu:
                    self.setups[k] = gpu_utils.send_to_gpu(np.array(v), d_type)

        # Update the options, to make sure there is no lib incompatibilities
        for k, v in self.options.items():
            self.update_option(k, self.options[k])

        self._on_gpu = on_gpu

    def update_setup(self, name, value):
        """Set the 'name' parameter in self.setups to the value 'value' given
        its type defined in setups.py. This is also sending it to GPU if we are
        on GPU mode.

        :param str name: The name of the parameter
        :param int, float, list, numpy.ndarray value: The value to attribute
        """
        if name not in bf_setups.INFO:
            raise AttributeError("Unknown setup name. Please pick one in "
                                 f"{bf_setups.INFO.keys()}.")

        if name == 'f_number' and isinstance(value, (int, float)):
            # Duplicate the f-number in both directions
            value = [value, value]

        self.setups[name] = self._convert_given_info(value,
                                                     bf_setups.INFO[name])

        if name in ['emitted_probe', 'received_probe'] and \
                'received_probe' in self.setups:
            ss = self.setups
            if self.on_gpu:
                self._is_same_probe = gpu_utils.all_equal(ss['emitted_probe'],
                                                          ss['received_probe'])
            else:
                self._is_same_probe = np.all(
                    [ss['emitted_probe'] == ss['received_probe']])

    def update_option(self, name, value):
        """Set the 'name' parameter in self.options to the value 'value' given
        its type defined in bf_options.INFO. This is also sending it to GPU if
        we are on GPU mode.

        :param str name: The name of the parameter
        :param float, str value: The value to attribute
        """
        if name not in bf_options.INFO:
            raise AttributeError("Unknown option name. Please pick an option "
                                 f"in {bf_options.INFO.keys()}.")

        # Make sure the option is valid based on the used lib
        enum_value = bf_options.factory(name, value)
        enum_value = self._checkup_lib_compatibility(name, enum_value)

        self.options[name] = self._convert_given_info(enum_value,
                                                      bf_options.INFO[name])

    def automatic_setup(self, acquisition_info, probe):
        """Loads the setups using a data file. It is the 'old' way for faked
        streamer, this might change in the future, or even be removed as it is
        very high level (expects data of given format, no control of what's
        been read, etc.). However, it is supposedly more flexible to new
        data... Need to find a trade-off here. The new setups are updated in
        the setup parameter of the class.

        :param dict acquisition_info: The setup of the acquisition system, see
            the Reader class to learn about the expected format
        :param Probe probe: The probe class, see the Reader class to check how
            it's been built
        """
        self.update_setup('sampling_freq', acquisition_info['sampling_freq'])
        self.update_setup('central_freq', probe.central_freq)
        if acquisition_info['sound_speed'] is not None:
            self.update_setup('sound_speed', acquisition_info['sound_speed'])
        if acquisition_info['t0'] is not None:
            self.update_setup('t0', acquisition_info['t0'])
        if acquisition_info['signal_duration'] is not None:
            self.update_setup('signal_duration',
                              acquisition_info['signal_duration'])
        if probe.bandwidth is not None:
            self.update_setup('bandwidth', probe.bandwidth)
        if acquisition_info['prf'] is not None:
            self.update_setup('prf', acquisition_info['prf'])
        seq = acquisition_info['sequence_elements']
        self.update_setup('emitted_probe', probe.geometry[:, seq['emitted']])
        self.update_setup('received_probe', probe.geometry[:, seq['received']])
        self._is_same_probe = np.all([seq['emitted'] == seq['received']])
        self.update_setup('transmissions_idx',
                          list(range(acquisition_info['delays'].shape[0])))
        self.update_setup('delays', acquisition_info['delays'])
        th = probe.get_thetas()
        self.update_setup('emitted_thetas', th[seq['emitted']])
        self.update_setup('received_thetas', th[seq['received']])

    def init_from_beamformer(self, beamformer):
        """Updates the setups and options using a previously initialized
        beamformer.

        :param Beamformer beamformer: Init the setups / options from another
            already initialized beamformer
        """
        self._is_iq = beamformer.is_iq
        self._on_gpu = beamformer.on_gpu
        self._is_same_probe = beamformer.is_same_probe
        for key, value in bf_setups.INFO.items():
            _, d_type, is_array = value
            if is_array and beamformer.on_gpu:
                self.update_setup(key, beamformer.setups[key].get())
            else:
                self.update_setup(key, beamformer.setups[key])
        for key, value in bf_options.INFO.items():
            self.update_option(key, beamformer.options[key])

    def compute_envelope(self, data, scan, method='demodulation', axis=-1,
                         bf_f0_ratio=1.):
        """Computes the envelope of our beamformed signal, on GPU or CPU based
        on the beamformer status. It is flexible to RFs or I/Qs, and can be
        performed using two methods (demodulation or hilbert) for RFs. The
        envelope is computed along the last axis.

        :param numpy.ndarray, cupy.array data: The beamformed array (either
            numpy array on CPU or a GPUArray on GPU)
        :param Scan scan: The scan used for the beamforming, mandatory to know
            the axial step
        :param str method: The method to use for the envelope computation (only
            on RFs, as envelope for I/Qs is only the modulo of the data). These
            could be demodulation (default) or hilbert.
        :param int axis: The axis on which to perform the envelope
        :param float bf_f0_ratio: Sometimes the beamformed signals are shifted
            to bf_f0_ratio x f0 (by 2 in FDMAS for example)

        :returns: The envelope of the beamformed data (floats)
        :return type: numpy.ndarray, cupy.array
        """
        if method not in ['demodulation', 'hilbert']:
            raise AttributeError(
                "Unknown method for computing the envelope. Should be "
                "demodulation or hilbert.")

        if self.on_gpu:
            if method == 'hilbert':
                raise NotImplementedError(
                    "No hilbert implementation for the envelope on GPU, "
                    "switch to 'demodulation' or to CPU mode.")

            return self._compute_envelope_gpu(data, scan, method, axis,
                                              bf_f0_ratio)
        else:
            return self._compute_envelope_cpu(data, scan, method, axis,
                                              bf_f0_ratio)

    def get_focused_data(self, pixel):
        """Computes the indices of the delays at a given position for a linear
        probe.

        :param tuple pixel: The position of the pixel to observe, it can be
            either in 2D or 3D

        :returns: The indices of the delays for each transmission and each
            element of the probe
        :return type: numpy.ndarray
        """
        if len(pixel) == 2:
            x, z = pixel
            y = 0
        elif len(pixel) == 3:
            x, y, z = pixel
        else:
            raise AttributeError("Pixel must be either 2D or 3D.")

        # Apertures
        delays = self.delays
        sound_speed = self.setups['sound_speed']
        f_number = self.setups['f_number']
        sampling_freq = self.setups['sampling_freq']
        t0 = self.t0

        # Distance of the emitted probe to the grid
        e_dist2x, e_dist2y, e_dists = get_distances(
            self.emitted_probe, np.array(x), np.array(y), np.array(z))
        r_dist2x, r_dist2y, r_dists = get_distances(
            self.received_probe, np.array(x), np.array(y), np.array(z))

        # If the emission also has an aperture, we set the distances
        # outside it to infinite, so they are never used
        if self.options['emitted_aperture'] == 1:
            e_ratio = get_aperture_ratio(np.array(z), e_dist2x, e_dist2y,
                                         e_dists, self.emitted_thetas, f_number)
            e_dists[abs(e_ratio) > 1] = np.Inf

        # Aperture of the received elements
        r_ratio = get_aperture_ratio(np.array(z), r_dist2x, r_dist2y, r_dists,
                                     self.received_thetas, f_number)
        r_dists[abs(r_ratio) > 1] = np.Inf

        # Transmission delays
        axes_to_expand = tuple(range(delays.ndim, e_dists.ndim))
        delays = np.expand_dims(delays, axis=axes_to_expand)
        transmission = np.min(delays * sound_speed + e_dists, axis=1)

        # Reception delays
        reception = r_dists

        # Compute the delays and get the data given the chosen interpolation
        # method
        tau = (reception + transmission[:, None]) / sound_speed
        indices = (tau - t0) * sampling_freq
        indices[indices == np.Inf] = -1

        return np.squeeze(indices, axis=2)

    def beamform(self, data, scan, *args, **kwargs):
        """The factory for beamforming method, based on GPU mode.
        """
        # Adjust the data if it should be either on CPU or GPU
        data = self._check_data_format(data)
        if data is None:
            return

        # Adjust the scan if it should be either on CPU or GPU
        self._check_scan_format(scan)

        if self.on_gpu:
            return self.beamform_gpu(data, scan, *args, **kwargs)
        else:
            return self.beamform_cpu(data, scan, *args, **kwargs)

    def beamform_packet(self, data, scan, *args, **kwargs):
        """The factory for beamform_packet method, based on GPU mode.
        """
        # Adjust the data if it should be either on CPU or GPU
        data = self._check_data_format(data)
        if data is None:
            return

        # Adjust the scan if it should be either on CPU or GPU
        self._check_scan_format(scan)

        if self.on_gpu:
            return self.beamform_packet_gpu(data, scan, *args, **kwargs)
        else:
            return self.beamform_packet_cpu(data, scan, *args, **kwargs)

    def beamform_gpu(self, *args, **kwargs):
        """The beamform method (on GPU) should be implemented in child classes.
        """
        raise NotImplementedError

    def beamform_cpu(self, *args, **kwargs):
        """The beamform method (on CPU) should be implemented in child classes.
        """
        raise NotImplementedError

    def beamform_packet_gpu(self, *args, **kwargs):
        """The beamform_packet method (on GPU) should be implemented in child
        classes.
        """
        raise NotImplementedError

    def beamform_packet_cpu(self, *args, **kwargs):
        """The beamform_packet method (on CPU) should be implemented in child
        classes.
        """
        raise NotImplementedError

    def _initialize_setups(self):
        """Initializes self.setups with the default values from setups.py.
        """
        for key, value in bf_setups.INFO.items():
            self.update_setup(key, value[0])

    def _initialize_options(self):
        """Initializes self.options with the basic options from options.py.
        Note that options can be updated by children right after this
        initialization.
        """
        for key, value in bf_options.INFO.items():
            self.update_option(key, value[0])

    def _checkup_lib_compatibility(self, option_name, option_value):
        """Checks if the current library used (numpy / numba on CPU and cupy on
        GPU) is compatible with the new selected option.

        :param str option_name: The name of the option to change
        :param int, float option_value: The value to update

        :returns: The new value for the option, that will work for sure
        :return type: int, float
        """
        if self.on_gpu:
            # Interpolation should be either none or linear
            if option_name == 'interpolation':
                if option_value > 1:
                    logger.warning(
                        "Only 'none' and 'linear' interpolation methods are "
                        "supported on GPU. Will perform DAS using linear "
                        "(default).")
                    option_value = 1

            # Incompatibility or unimplemented methods for cupy lib
            if cfg.CPU_LIB == 'cupy':
                # Add here the incompatibilities with the cupy lib
                pass

        else:
            # Incompatibility or unimplemented methods for numpy lib
            if cfg.CPU_LIB == 'numpy':
                # Only boxcar apodization is supported using numpy
                if option_name == 'rx_apodization':
                    if option_value > 0:
                        logger.warning(
                            "Apodization at reception is not implemented for "
                            "Numpy, the default value 'boxcar' will be used "
                            "instead.")
                        option_value = 0

            # Incompatibility or unimplemented methods for numba lib
            if cfg.CPU_LIB == 'numba':
                # Add here the incompatibilities with the Numba lib
                pass

        return option_value

    def _convert_given_info(self, value, info):
        """Returns the value in a proper format for GPU if needed.

        :param int, float, numpy.ndarray value: The value to attribute
        :param tuple info: The info for this value (default, dtype, is_array)

        :returns: The value (converted if relevant)
        :return type: int, float, numpy.ndarray, numpy.int32, numpy.float32,
            cupy.array
        """
        _, d_type, is_array = info
        if self.on_gpu:
            if is_array:
                return gpu_utils.send_to_gpu(np.array(value), d_type)
            else:
                return d_type(value)
        else:
            if is_array:
                return np.array(value, dtype=d_type)
            else:
                return d_type(value)

    def _check_data_format(self, data):
        """Makes sure the data format is ok for beamforming. Two checks are
        made here:

            - check if the data is on CPU / GPU based on the requested mode
            - check if the data is complex if is on I/Qs mode

        :param numpy.ndarray, cupy.array data: The data stored either on GPU or
            CPU

        :returns: The data in a proper format, or None if unknown situation.
        :return type: None, numpy.ndarray, cupy.array
        """
        # IF GPU mode but the data is on CPU, actually not a warning as data is
        # supposed to change for each beamforming, so it doesn't need to be
        # sent to GPU beforehand
        if self.on_gpu and isinstance(data, np.ndarray):
            logger.info(f"Needs to send the data to the GPU.")
            dtype = np.complex64 if self.is_iq else np.float32
            data = gpu_utils.send_to_gpu(data, dtype)

        # IF CPU mode but the data is on GPU, the user probably wants to use
        # the GPU mode but somehow doesn't, calls a warning and send the data
        # to CPU
        elif not self.on_gpu and not isinstance(data, np.ndarray):
            logger.warning("Data needs to be on CPU for CPU mode, will get it"
                           "back.")
            try:
                data = data.get()
            except AttributeError:
                logger.error("Unknown data format, please set it to either "
                             "numpy array (CPU) or cupy array (GPU).")
                return None

        # If it should work on I/Qs, expects the data to be of a complex type
        if self.is_iq and not np.iscomplexobj(data):
            logger.error("The data are expected to be I/Qs, Use the rf2iq "
                         "method to convert them.")
            return None

        return data

    def _check_scan_format(self, scan):
        """Makes sure the scan is either on CPU or GPU based on the beamforming
        mode.

        :param Scan scan: The Scan with the pixels to beamform information
        """
        # Checks if the scan mode matches the beamforming mode
        if self.on_gpu != scan.on_gpu:
            logger.warning(f"Wrong mode for Scan object, switched to "
                           f"{'GPU' if self.on_gpu else 'CPU'} mode.")
            scan.set_on_gpu(self.on_gpu)

    def _compute_envelope_gpu(self, d_data, scan, method='demodulation',
                              axis=-1, bf_f0_ratio=1.):
        """Computes the envelope of our beamformed signal. It is flexible to
        RFs or I/Qs.

        :param numpy.ndarray, cupy.array d_data: The GPUArray data stored on
            GPU, of dtype complex64
        :param Scan scan: The scan used for the beamforming, mandatory to know
            the axial step
        :param str method: The method to use for the envelope computation (only
            on RFs, as envelope for I/Qs is only the modulo of the data). It
            can only be set to 'demodulation' on GPU
        :param int axis: The axis on which to perform the envelope
        :param float bf_f0_ratio: Sometimes the beamformed signals are shifted
            to bf_f0_ratio x f0 (by 2 in FDMAS for example)

        :returns: The envelope of the beamformed data (floats).
        :return type: numpy.ndarray, cupy.array
        """
        # Output on GPU, with proper type (float)
        d_output = gpu_utils.initialize_empty(d_data.shape, np.float32)
        g_dim, b_dim = gpu_utils.compute_flat_grid_size(d_data.size)

        # If we're working with RFs
        if not self.is_iq:
            # Sampling frequency of the beamformed signals
            delta_axial = (1 / scan.axial_step)
            beamformed_fs = delta_axial * self.setups['sound_speed'] / 2

            # The central frequency of the beamformed signals is most of the
            # time still centered at f0, but can be rotated in some case
            # (ex: FDMAS)
            beamformed_f0 = self.setups['central_freq'] * bf_f0_ratio

            # Initial time based on axial axis, set to zero, not sure if it is
            # the good way, doesn't change a lot tho
            # beamformed_t0 = scan_z_axis[0] / beamformed_fs
            beamformed_t0 = 0

            if beamformed_fs < beamformed_f0:
                raise ValueError(
                    "The spatial display frequency is too low, please "
                    "increase the axial resolution or switch to I/Qs.")
            us.rf2iq(d_data, beamformed_f0, beamformed_fs, beamformed_t0,
                     bandwidth=self.setups['bandwidth'], axis=axis)

        # Get modulo of the beamformed signals
        k_get_modulo(g_dim, b_dim, (d_data, np.uint32(d_data.size), d_output))

        return d_output

    def _compute_envelope_cpu(self, data, scan, method='demodulation', axis=-1,
                              bf_f0_ratio=1.):
        """Computes the envelope of our beamformed signal. It is flexible to
        RFs or I/Qs, and can be performed using two methods (demodulation or
        hilbert) for RFs. The envelope is computed along the last axis by
        default.

        :param numpy.ndarray data: The beamformed data, it can be
            multidimensional (in case of 3D B-mode)
        :param Scan scan: The scan used for the beamforming, mandatory to know
            the axial step
        :param str method: The method to use for the envelope computation (only
            on RFs, as envelope for I/Qs is only the modulo of the data). These
            could be demodulation (default) or hilbert
        :param int axis: The axis on which to compute the envelope
        :param float bf_f0_ratio: Sometimes the beamformed signals are shifted
            to bf_f0_ratio x f0 (by 2 in FDMAS for example)

        :returns: The envelope of the beamformed data (floats).
        :return type: numpy.ndarray
        """
        if method not in ['demodulation', 'hilbert']:
            raise AttributeError("Unknown method for computing the envelope. "
                                 "Should be demodulation or hilbert.")

        # If we're working with RFs
        if not self.is_iq:
            # Sampling frequency of the beamformed signals
            delta_axial = (1 / scan.axial_step)
            beamformed_fs = delta_axial * self.setups['sound_speed'] / 2

            # The central frequency of the beamformed signals is most of the
            # time still centered at f0, but can be rotated in some case
            # (ex: FDMAS)
            beamformed_f0 = self.setups['central_freq'] * bf_f0_ratio

            # Initial time based on axial axis, set to zero, not sure if it is
            # the good way, doesn't change a lot tho
            # beamformed_t0 = scan_z_axis[0] / beamformed_fs
            beamformed_t0 = 0

            if method == 'demodulation':
                if beamformed_fs < beamformed_f0:
                    raise ValueError(
                        "The spatial display frequency is too low, please "
                        "increase the axial resolution or switch to I/Qs.")
                data = us.cpu.rf2iq(
                    data, beamformed_f0, beamformed_fs, beamformed_t0,
                    bandwidth=self.setups['bandwidth'], axis=axis)
            else:
                smooth = scipy.signal.tukey(data.shape[axis], 1e-4)
                shp = np.ones(data.ndim, dtype=int)
                shp[axis] = -1
                data *= smooth.reshape(shp)
                ratio = (self.setups['bandwidth'] / 100) / 2
                fc1 = beamformed_f0 - (self.setups['central_freq'] * ratio)
                fc2 = beamformed_f0 + (self.setups['central_freq'] * ratio)
                data = us.cpu.filtfilt(data, fc1, beamformed_fs,
                                       'high', axis=axis)
                data = us.cpu.filtfilt(data, fc2, beamformed_fs,
                                       'low', axis=axis)
                data = scipy.signal.hilbert(data)

        # Get modulo of the beamformed signals
        data = np.abs(data)

        return data
