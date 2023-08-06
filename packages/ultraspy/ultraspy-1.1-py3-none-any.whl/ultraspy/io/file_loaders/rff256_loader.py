"""Loader for .rff256 data, reads all the data and recovers it based on the
format of the data.
TODO: Clean up the code, especially when we have many plane waves. Also should
      check the data from Andrei.
"""
import os
import io
import configparser
import re

from array import array
import numpy as np

from scipy.signal import butter, filtfilt

from .file_loader import FileLoader
from ...utils.string import remove_comments


class Rff256Loader(FileLoader):
    """Rff256Loader class, reads the data and helps to recover. Inherit from
    FileLoader class. It is using three files (or even more in case of multiple
    plane waves imaging), but expects the data file here (.rff256). From there,
    it'll recover the params file (.uop), the configs file (.uos).

    :ivar int nb_boards: The number of boards in the UlaOp system
    :ivar bool filter_low_freqs: If the hardware high-pass filter was triggered
    :ivar str data_file: The data file path
    :ivar str params_file: The parameters file path
    :ivar str configs_file: The configuration file path
    """

    def __init__(self, filepath):
        """Parent initializer, then load the mat file into the data dict.

        :param str filepath: The path where to find the data (.rff256)
        """
        super().__init__(filepath)
        # TODO: Not always the same as the one in the config file, should be
        self.nb_boards = 4
        self.filter_low_freqs = False

        directory, data_file = os.path.split(filepath)
        basename = '_'.join(data_file.split('_')[:-1])
        configs_file = os.path.splitext(data_file)[0] + '.uos'
        params_file = basename + '_params.uop'
        self.data_file = filepath
        self.params_file = os.path.join(directory, params_file)
        self.configs_file = os.path.join(directory, configs_file)

        nb_pw = self.get_nb_plane_waves()
        params = None
        configs = None
        angles = []
        if nb_pw == 1:
            params = self.extract_params()
            configs = self.extract_configs()
            data = self.extract_data(configs['nb_data'])
            data = self.reorganize_data(data, params, self.filter_low_freqs)
            data = data[:, None]
            angles = [0]
        else:
            data = []
            for n in range(nb_pw):
                params = self.extract_params(n)
                angles.append(params['angle'])
                file_name = basename + '_SliceRFPre' + str(n + 1)
                self.data_file = os.path.join(directory, file_name + '.rff256')
                self.configs_file = os.path.join(directory, file_name + '.uos')
                configs = self.extract_configs()
                _data = self.extract_data(configs['nb_data'])
                data.append(self.reorganize_data(_data, params,
                                                 self.filter_low_freqs))
            data = np.array(data).transpose([1, 0, 2, 3])

        self.data = {
            'params':  params,
            'configs': configs,
            'data':    data,
            'angles':  angles,
        }

    def parse_config_file(self):
        """Parses the config file.

        :returns: The config extracted from the params file
        :return type: configparser.ConfigParser
        """
        s_config = open(self.params_file, 'r').read()
        s_config = remove_comments(s_config)
        buf = io.StringIO(s_config)
        config = configparser.ConfigParser()
        config.read_file(buf)
        return config

    def get_nb_plane_waves(self):
        """Reads the .uop file and get the number of plane waves.

        :returns: The number of plane waves
        :return type: int
        """
        config = self.parse_config_file()
        nb_pw = 1
        while 'Item' + str(nb_pw) in config['SEQUENCER']:
            nb_pw += 1
        return nb_pw

    def extract_params(self, item=0):
        """Reads the .uop file and get the params from it.

        :param int item: The item to focus on (the plane wave to study when we
            are doing plane wave imaging with compounding). It is set to 0 by
            default, for the case where we only have one plane wave.

        :returns: A dictionary with the info extracted from the parameters file
        :return type: dict
        """
        config = self.parse_config_file()

        gen = config['WORKINGSET']
        hardware_set = config['HARDWARE']
        ssg_set = config['SSG']
        reception_set = config['RXSETTINGS@item' + str(item)]
        emission_set = config['TXSETTINGS@item' + str(item)]
        acquisition_set = config['ACQUIRERF_PRE']
        slice_name = 'Slice' + str(item)

        return {
            'pitch': int(re.findall(r'\d+', gen['ProbeParameters'])[1]) * 1e-7,
            'sound_speed': gen.getint('SoundSpeed'),
            'angle': emission_set.getfloat('TXAngle'),
            'prf': ssg_set.getint('Prf'),
            'ry_min': reception_set.getfloat('RYMin') * 1e-3,
            'ry_max': reception_set.getfloat('RYMax') * 1e-3,
            'tx_freq': emission_set.getfloat('TXFreq'),
            'nb_gates': int(acquisition_set[slice_name].split(', ')[0]),
            'nb_ts': int(acquisition_set[slice_name].split(', ')[0]),
            'downsampled': int(hardware_set['SysDownsampling']),
        }

    def extract_configs(self):
        """Reads the .uos file and get the configs from it.

        :returns: A dictionary with the info extracted from the config file
        :return type: dict
        """
        s_config = open(self.configs_file, 'r').read()
        s_config = remove_comments(s_config)
        buf = io.StringIO(s_config)
        config = configparser.ConfigParser()
        config.read_file(buf)

        gen = config['Info']

        return {
            'nb_data': gen.getint('TotalSize'),
        }

    def extract_data(self, nb_data):
        """Reads the .rff256 file and get the data from it.

        :param int nb_data: The number of data bytes to extract

        :returns: The raw data from the data file
        :return type: np.ndarray
        """
        data = array('b')
        with open(self.data_file, 'rb') as f:
            data.fromfile(f, nb_data)
        return np.array(data)

    def reorganize_data(self, data, params, filter_low_freqs):
        """Reshaping process.

        :param numpy.ndarray data: The data we've extracted
        :param dict params: The parameters of the data
        :param bool filter_low_freqs: If True, we filter the very low frequency
            noises (< 0.05% of nyquist frequency)

        :returns: The reorganized data based on the parameters of the
            acquisition
        :return type: np.ndarray
        """
        # Conversion due to bytes arrangement, not sure what's going on here
        # tho.... Refer to the matlab post-processing code provided by ula-op
        data = data.reshape((48, -1), order='F').astype(np.int16)
        ldiv = data[32:] & 15
        mdiv = (data[32:] >> 4) & 15
        data = np.concatenate([ldiv, mdiv], axis=0) + 16 * data[:32]

        # Reshape given our experiment
        data = data.reshape((16, params['nb_ts'], 2, self.nb_boards, -1),
                            order='F')
        data = np.concatenate([data[:, :, 0], data[:, :, 1]], axis=0)
        data = data.transpose([0, 2, 1, 3])
        data = data.reshape((32 * self.nb_boards, params['nb_ts'], -1),
                            order='F')
        if filter_low_freqs:
            b, a = butter(5, 0.05, btype='high')
            data = filtfilt(b, a, data, axis=1)
        return data.transpose([2, 0, 1])
