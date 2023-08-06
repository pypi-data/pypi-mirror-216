"""Reader class.
"""
import logging
import numpy as np

from ultraspy.io.file_loaders.factory import get_file_loader
from ultraspy.probes.factory import get_probe, build_probe, build_probe_from_geometry
from ultraspy.helpers.transmit_delays_helpers import compute_pw_delays
from ..utils.print import dict_to_list_str


logger = logging.getLogger(__name__)


class Reader(object):
    """Reader class to handle the data files from different ultrasound systems.
    After initialization, it has three attributes: the data itself, the
    data_info, and the probe class, which can be used directly in the Beamformer
    class. Check their getters to learn more about them. You also can call
    :code:`Reader.available_systems` to have the list of the implemented
    ultrasound systems.

    Currently, the supported systems are:

        - ultraspy: reads data formatted for the ultraspy library
        - picmus: reads data issued from the PICMUS challenge (
          creatis.insa-lyon.fr/Challenge/IEEE_IUS_2016)
        - must: reads the rotating disk data from MUST (biomecardio.com/MUST)
        - simus: data generated using the simulation tool SIMUS (biomecardio),
          contained RF and param
        - simu_3d: reads simulated 3d data from FieldII
        - dbsas: reads the data saved with the PA2 system of the company
          DB-SAS. It also works with the PAMini with some adaptations of the
          way it saves data
        - vera: reads data saved by the verasonics Vantage system, the saved
          workspace needs to have some specific variables (RcvData, Trans,
          Receive, Resource, PRF and P. It hasn't been tested in many
          situations, so for now, you should assume it'll only work on
          plane-waves emissions, with regular parameters
        - ulaop: reads data saved by the UlaOp system (from the MSD lab). This
          one is very high level and has been proven not to work in some
          situations (those should be checked some day). It should work fine on
          plane wave emissions (no focus) though.

    :cvar list available_systems: The list of the available systems
    :ivar dict data: The data, of shape (nb_frames, nb_plane_waves,
        nb_elements, nb_time_samples). The number of elements can be 1D or
        2D when we are using a 3D probe
    :ivar dict data_info: The information about the data
    :ivar dict acquisition_info: The information about the acquisition setup
    :ivar dict probe: The probe class
    """
    available_systems = [
        'ultraspy',
        'picmus',
        'must',
        'simus',
        'simu_3d',
        'dbsas',
        'vera',
        'ulaop',
    ]

    def __init__(self, data_file, system='ultraspy', verbose=True):
        """It initializes the Reader class, using a given data file, known for
        being recorded using a given system.

        :param str data_file: The path where to find the data
        :param str system: The name of the system to use, default is the data
            formatted for this library
        :param bool verbose: If True, we print a recap of the loaded data and
            of what has been extracted
        """
        if system not in self.available_systems:
            raise AttributeError(
                f"Unknown system ({system}), please pick one among: "
                f"{self.available_systems}.")

        # The useful attributes for our classes
        self.data = None
        self.data_info = {}
        self.acquisition_info = {}
        self.probe = None

        # Get the file loader given the extension of our data file
        file_loader = get_file_loader(data_file)
        self.__extract_data(file_loader.data, system)

        # Print results
        if verbose:
            # print(file_loader)
            print(self)

    def get_data(self):
        """Returns the extracted data (of shape: (nb_frames, nb_transmissions,
        nb_elements, nb_time_samples))

        :returns: The Numpy array with the ultrasound data
        :return type: numpy.ndarray
        """
        return self.data

    def get_data_info(self):
        """Returns the information related to the data, which contains:

            - data_shape: tuple of int
            - data_type: the type of the data
            - is_iq: bool

        :returns: The information about the data
        :return type: dict
        """
        return self.data_info

    def get_acquisition_info(self):
        """Returns the information related to the acquisition, which contains:

            - sampling_freq: in Hz
            - t0: in s
            - prf: in Hz
            - signal_duration: in s
            - delays: in m/s
            - sound_speed: in m/s

        :returns: The information about the acquisition
        :return type: dict
        """
        return self.acquisition_info

    def get_probe(self):
        """Returns the probe class, which contains (mainly):

            - geometry: of shape (nb_dim, nb_elements)
            - central_freq: in Hz
            - bandwidth: in percentage

        :returns: The information about the probe
        :return type: Probe
        """
        return self.probe

    def __str__(self):
        """String sentence to show the data characteristics. Note that it is
        using pretty_print functions, not all data are displayed for ease of
        read.

        :returns: A pretty print to display info about the Reader class
        :return type: str
        """
        return '\n'.join([
            '====== Loaded: ======',
            'Data looking like:',
            '\n'.join(dict_to_list_str(self.data_info, 2)),
            'Acquired with the settings:',
            '\n'.join(dict_to_list_str(self.acquisition_info, 2)),
            'Using the probe:',
            str(self.probe),
        ])

    def __extract_data(self, loaded_dict, system):
        """Factory, selects the good data format based on the system.

        :param dict loaded_dict: The dictionary we've extracted from the data
            file
        :param str system: The name of the system that has been used options

        :returns: The proper method to extract data
        :return type: function
        """
        return {
            'ultraspy': self.__extract_ultraspy_data,
            'picmus': self.__extract_picmus_data,
            'must': self.__extract_must_data,
            'simus': self.__extract_simus_data,
            'simu_3d': self.__extract_simu_3d_data,
            'dbsas': self.__extract_dbsas_data,
            'vera': self.__extract_vera_data,
            'ulaop': self.__extract_ulaop_data,
        }[system](loaded_dict)

    def __extract_ultraspy_data(self, loaded_dict):
        """Extracts the relevant data, considering it has the format of the
        ultraspy lib.

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        # Get the output data
        data = loaded_dict['output']['data']

        # Build the probe
        probe_name = loaded_dict['probe']['name'].decode('utf-8')
        if probe_name is not None:
            probe = get_probe(probe_name)
        else:
            geometry = loaded_dict['probe']['geometry']
            probe = build_probe_from_geometry(
                geometry[0, :], geometry[1, :], geometry[2, :],
                loaded_dict['probe']['central_freq'],
                loaded_dict['probe']['bandwidth'])

        # Sequences
        emitted_sequence = loaded_dict['sequence']['emitted']
        received_sequence = loaded_dict['sequence']['received']

        # Acquisition
        sampling_freq = loaded_dict['acquisition']['sampling_freq']
        t0 = loaded_dict['acquisition']['t0']
        prf = loaded_dict['acquisition']['prf']
        signal_dur = loaded_dict['acquisition']['signal_duration']
        sound_speed = loaded_dict['acquisition']['sound_speed']
        delays = loaded_dict['acquisition']['delays']

        # self.data = data.astype(np.int32)
        self.data = data.astype(np.float32)
        self.data_info = {
            'data_shape': data.shape,
            'data_type': np.float32,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': sampling_freq,
            't0': t0,
            'prf': prf,
            'signal_duration': signal_dur,
            'delays': delays,
            'sound_speed': sound_speed,
            'sequence_elements': {
                'emitted': emitted_sequence,
                'received': received_sequence,
            }
        }
        self.probe = probe

    def __extract_picmus_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from Picmus.

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        dataset = loaded_dict['US']['US_DATASET0000']

        # Identify the type of the data
        is_iq = dataset['data']['imag'].any()

        # Recover the data based on the format (I/Q, or RF)
        data = dataset['data']['real']
        angles = dataset['angles']

        probe = get_probe('L11-4v')
        file_f0 = dataset['sampling_frequency'][0] / 4
        if probe.central_freq != file_f0:
            logger.warning("The central frequency does not match the probe, "
                           f"update to {file_f0}, was {probe.central_freq}.")
            probe.set_central_freq(file_f0)

        # If is I/Q, needs to add the imaginary components to the data
        if is_iq:
            data = data.astype(np.complex64) + 1j * dataset['data']['imag']
            if probe.central_freq != dataset['modulation_frequency'][0]:
                logger.warning("The modulation frequency used for down-mixing "
                               "is not a fourth of the sampling frequency.")
                probe.set_central_freq(dataset['modulation_frequency'][0])

        # Compute the delays, in PICMUS, they are centered 2D plane waves
        speed_of_sound = dataset['sound_speed'][0]
        delays = compute_pw_delays(angles, probe,
                                   speed_of_sound=speed_of_sound,
                                   transmission_mode='centered',
                                   smallest=False)

        # Adds an extra dimension for the number of frames (only one here)
        data = data[None, :]
        nb_transmissions = delays.shape[0]
        elements_indices = np.arange(probe.nb_elements)

        self.data = data
        self.data_info = {
            'data_shape': data.shape,
            'data_type': data.dtype,
            'is_iq': is_iq,
        }
        self.acquisition_info = {
            'sampling_freq': dataset['sampling_frequency'][0],
            't0': dataset['initial_time'][0],
            'prf': dataset['PRF'][0],
            'signal_duration': 0.5 * 1e-6,
            'delays': delays,
            'sound_speed': speed_of_sound,
            'sequence_elements': {
                'emitted': np.tile(elements_indices, (nb_transmissions, 1)),
                'received': np.tile(elements_indices, (nb_transmissions, 1)),
            }
        }
        self.probe = probe

    def __extract_must_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from MUST
        (Damien).

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        # Build the probe
        probe = get_probe('L7-4')
        probe.set_central_freq(loaded_dict['param']['fc'])
        probe.set_bandwidth(loaded_dict['param']['bandwidth'])

        # Compute the delays, only one plane wave here, so should be all 0
        speed_of_sound = loaded_dict['param']['c']
        delays = loaded_dict['param']['TXdelay'][None, :]
        nb_transmissions = delays.shape[0]
        elements_indices = np.arange(probe.nb_elements)

        self.data = loaded_dict['RF'].transpose(2, 1, 0)[:, None, :]
        self.data_info = {
            'data_shape': self.data.shape,
            'data_type': self.data.dtype,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': loaded_dict['param']['fs'],
            't0': loaded_dict['param']['t0'],
            'prf': loaded_dict['param']['PRF'],
            'signal_duration': None,
            'delays': delays,
            'sound_speed': speed_of_sound,
            'sequence_elements': {
                'emitted': np.tile(elements_indices, (nb_transmissions, 1)),
                'received': np.tile(elements_indices, (nb_transmissions, 1)),
            }
        }
        self.probe = probe

    def __extract_simus_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from the SIMUS
        tool from biomecardio.

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        # Build the probe
        probe = get_probe(loaded_dict['param']['probe_name'])

        # Different process if only one transmission or more
        data = loaded_dict['RF']
        delays = loaded_dict['param']['delays']
        if delays.ndim == 1:
            data = data.T[None, :, :]
            delays = delays[None, :]
        else:
            data = data.transpose(2, 1, 0)
        nb_transmissions = delays.shape[0]
        elements_indices = np.arange(probe.nb_elements)

        self.data = data[None, ...]
        self.data_info = {
            'data_shape': self.data.shape,
            'data_type': self.data.dtype,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': loaded_dict['param']['fs'],
            't0': 0,
            'prf': None,
            'signal_duration': None,  # 1 / probe.central_freq,
            'delays': delays,
            'sound_speed': 1540,
            'sequence_elements': {
                'emitted': np.tile(elements_indices, (nb_transmissions, 1)),
                'received': np.tile(elements_indices, (nb_transmissions, 1)),
            }
        }
        self.probe = probe

    def __extract_simu_3d_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from Field II
        simulation code of the US toolbox.

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        # Build the probe
        probe = get_probe(loaded_dict['param']['probe_name'])

        # Different process if only one transmission or more
        data = loaded_dict['RF']
        delays = loaded_dict['param']['delays']
        if delays.ndim == 1:
            data = data.T[None, :, :]
            delays = delays[None, :]
        else:
            data = data.transpose(2, 1, 0)
        nb_transmissions = delays.shape[0]
        elements_indices = np.arange(probe.nb_elements)

        self.data = data[None, ...]
        self.data_info = {
            'data_shape': self.data.shape,
            'data_type': self.data.dtype,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': loaded_dict['param']['fs'],
            't0': loaded_dict['param']['t0'],
            'prf': None,
            'signal_duration': None,  # 1 / probe.central_freq,
            'delays': delays,
            'sound_speed': 1540,
            'sequence_elements': {
                'emitted': np.tile(elements_indices, (nb_transmissions, 1)),
                'received': np.tile(elements_indices, (nb_transmissions, 1)),
            }
        }
        self.probe = probe

    def __extract_dbsas_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from the DB-SAS
        system. There's a lot of unprocessed information here. You can check it
        out by using the print function of the FileLoader. In a nutshell:

            - TFMdata (expected output image, provided by from db-sas system)
            - spaceGrid (the information about the reconstructed grid)
            - output (the data over the time (it's a video, not many angles),
              + the position of the probes for every frame)
            - setup (lots of unused data, like the information about the Impulse
              Response, the data about the elements, the time vector, etc.)

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        data = loaded_dict['output']['dataEncoder']
        # angles = np.concatenate([loaded_dict['setup']['dTheta1'],
        #                          loaded_dict['setup']['dTheta2']])
        # angles = np.radians(angles)
        delays = loaded_dict['setup']['tau'].T * 1e-6
        nb_frames = data.shape[0]
        nb_time_samples = data.shape[-1]
        data = data.reshape(nb_frames, delays.shape[0], -1, nb_time_samples)
        speed_of_sound = loaded_dict['setup']['cL'][0, 0] * 1e3
        del_s = 2 * (loaded_dict['setup']['dDel'][0, 0] / speed_of_sound)
        ind_del = round(del_s * loaded_dict['setup']['Fs'][0, 0])
        data[:, :, :, :ind_del] = 0
        central_freq = loaded_dict['setup']['Fcenter'][0, 0] * 1e6
        if 'AWG_pulseDuration' in loaded_dict['setup']:
            sig_dur = loaded_dict['setup']['AWG_pulseDuration'][0, 0] * 1e-6
        else:
            sig_dur = 1 / central_freq
        _, nb_t, nb_e, _ = data.shape

        # If we got the name of the probe (preferred way)
        if 'probe_name' in loaded_dict['setup']:
            probe = get_probe(loaded_dict['setup']['probe_name'])

        # If we didn't, there should be the probe geometry within probeT
        elif 'probeT' in loaded_dict:
            x = np.squeeze(loaded_dict['probeT']['X']) * 1e-3
            y = np.squeeze(loaded_dict['probeT']['Y']) * 1e-3
            z = np.squeeze(loaded_dict['probeT']['Z']) * 1e-3
            if np.min(x) >= 0:
                x = (x + np.min(x)) - (np.max(x) - np.min(x)) / 2
            probe = build_probe_from_geometry(x, y, z, central_freq)

        # If we don't have anything, high level linear probe using the pitch
        else:
            pitch = loaded_dict['setup']['dx_p1'][0, 0] * 1e-3
            probe = build_probe('linear', nb_e, pitch, central_freq)

        # # Compute the delays using the probe
        # delays = compute_pw_delays(angles, probe,
        #                            speed_of_sound=speed_of_sound)

        # Only deals with standard STA or PW, should be more flexible to any
        # elements location
        if nb_e == nb_t:
            # STA mode, 1 element emit, all receive
            emitted = np.arange(probe.nb_elements)[:, None]
            received = np.tile(np.arange(probe.nb_elements), (nb_t, 1))
        else:
            # Plane wave mode, emission = reception sequence
            emitted = np.tile(np.arange(probe.nb_elements), (nb_t, 1))
            received = np.tile(np.arange(probe.nb_elements), (nb_t, 1))

        # self.data = data.astype(np.int32)
        self.data = data.astype(np.float32)
        self.data_info = {
            'data_shape': data.shape,
            'data_type': data.dtype,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': loaded_dict['setup']['Fs'][0, 0] * 1e6,
            't0': loaded_dict['setup']['startTime'][0, 0] * 1e-6,
            'prf': int(1 / (loaded_dict['setup']['timeSlot'][0, 0] * 1e-6)),
            'signal_duration': sig_dur,
            'delays': np.take(delays, emitted),
            'sound_speed': speed_of_sound,
            'sequence_elements': {
                'emitted': emitted,
                'received': received,
            }
        }
        self.probe = probe

    def __extract_vera_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from the Vera
        echograph (.mat).

        TODO: Should not work anymore, not flexible to probes / delays

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        if 'Connector' in loaded_dict['Trans']:
            pin_map = [x - 1 for x in loaded_dict['Trans']['Connector']]
        else:
            nb_e = loaded_dict['Resource']['Parameters']['numTransmit']
            pin_map = list(range(nb_e))
        data = loaded_dict['RcvData'][:, pin_map]
        # If single frame
        if len(data.shape) == 2:
            data = data[..., None]
        if 'angles' not in loaded_dict:
            angles = np.array([0.0])
        else:
            angles = np.ravel([loaded_dict['angles']])
        nb_a = len(angles)
        _, nb_e, nb_f = data.shape
        sample = loaded_dict['Receive']
        if nb_f > 1:
            nb_t = sample[0].endSample - sample[0].startSample
            reshaped = np.zeros((nb_t, nb_e, nb_f, nb_a))
            for f in range(nb_f):
                for a in range(len(angles)):
                    idx = a + (f - 1) * len(angles)
                    start = loaded_dict['Receive'][idx].startSample
                    end = loaded_dict['Receive'][idx].endSample
                    reshaped[:, :, f, a] = data[start:end, :, f]
        else:
            nb_t = sample['endSample'] - sample['startSample']
            reshaped = np.zeros((nb_t, nb_e, nb_f, nb_a))
            for a in range(len(angles)):
                start = loaded_dict['Receive']['startSample']
                end = loaded_dict['Receive']['endSample']
                reshaped[:, :, 0, a] = data[start:end, :, 0]

        data = reshaped.transpose([2, 3, 1, 0])

        speed_of_sound = loaded_dict['Resource']['Parameters']['speedOfSound']
        central_freq = loaded_dict['Trans']['frequency'] * 1e6
        if nb_f > 1:
            fs = central_freq * sample[0].samplesPerWave
        else:
            fs = central_freq * sample['samplesPerWave']
        bounds = loaded_dict['Trans']['Bandwidth'] * 1e6
        bandwidth = abs(bounds[1] - bounds[0]) * 100 / central_freq

        # Build the probe
        pitch = loaded_dict['Trans']['spacingMm'] * 1e-3
        # probe_geometry = np.zeros(3, nb_e)
        # probe_geometry[0, :] = ((np.arange(nb_e) - ((nb_e - 1) / 2)) * pitch)
        # TODO: Super high level, but not sure how to do it differently
        geometry_type = 'linear'
        probe = build_probe(geometry_type, nb_e, pitch, central_freq,
                            bandwidth=bandwidth)

        # Compute the delays
        # TODO: Should check if they arent in the data
        delays = compute_pw_delays(angles, probe,
                                   speed_of_sound=speed_of_sound)

        # The PRF and t0 were added lately in my saved workspaces... Those
        # might be missing
        prf = None
        if 'PRF' in loaded_dict:
            prf = loaded_dict['PRF']
        t0 = None
        if 'P' in loaded_dict:
            sample_dist = speed_of_sound / central_freq
            z_min = loaded_dict['P']['startDepth'] * sample_dist
            t0 = z_min * 2 / speed_of_sound

        self.data = data
        self.data_info = {
            'data_shape': data.shape,
            'data_type': data.dtype,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': fs,
            't0': t0,
            'prf': prf,
            'signal_duration': None,
            'delays': delays,
            'sound_speed': speed_of_sound,
            'sequence_elements': {
                'emitted': np.tile(np.arange(probe.nb_elements), (nb_a, 1)),
                'received': np.tile(np.arange(probe.nb_elements), (nb_a, 1)),
            }
        }
        self.probe = probe

    def __extract_ulaop_data(self, loaded_dict):
        """Extracts the relevant data, considering it is coming from the Ula-Op
        echograph (rff256). Currently only works for RFs.

        TODO: Should not work anymore, not flexible to probes / delays

        :param dict loaded_dict: The dictionary extracted from the data file
        """
        speed_of_sound = loaded_dict['params']['sound_speed']
        data = loaded_dict['data']
        angles = np.radians(loaded_dict['angles'])
        ulaop_fs = 78.125 * 1e6
        real_fs = ulaop_fs / loaded_dict['params']['downsampled']

        # Build the probes
        # TODO: Super high level, but not sure how to do it differently
        geometry_type = 'linear'
        _, nb_t, nb_e, _ = data.shape
        pitch = loaded_dict['params']['pitch']
        central_freq = loaded_dict['params']['tx_freq']
        probe = build_probe(geometry_type, nb_e, pitch, central_freq)
        # probe_geometry = np.zeros(3, nb_e)
        # probe_geometry[0, :] = ((np.arange(nb_e) - ((nb_e - 1) / 2)) * pitch)

        # Compute the delays
        # TODO: Should check if they arent in the data
        delays = compute_pw_delays(angles, probe,
                                   speed_of_sound=speed_of_sound)

        self.data = data
        self.data_info = {
            'data_shape': data.shape,
            'data_type': data.dtype,
            'is_iq': False,
        }
        self.acquisition_info = {
            'sampling_freq': real_fs,
            't0': (loaded_dict['params']['ry_min'] / speed_of_sound) * 2,
            'prf': loaded_dict['params']['prf'],
            'signal_duration': None,
            'delays': delays,
            'sound_speed': speed_of_sound,
            'sequence_elements': {
                'emitted': np.tile(np.arange(probe.nb_elements), (nb_t, 1)),
                'received': np.tile(np.arange(probe.nb_elements), (nb_t, 1)),
            }
        }
        self.probe = probe
