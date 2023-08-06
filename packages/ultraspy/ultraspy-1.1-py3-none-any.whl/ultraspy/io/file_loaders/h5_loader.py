"""Loader for h5 data, reads all the data and recovers it based on the format
of the data.
"""
import h5py
import logging
import numpy as np

from .file_loader import FileLoader


logger = logging.getLogger(__name__)


class H5Loader(FileLoader):
    """H5Loader class, reads the data and helps to recover. Inherit from
    FileLoader class. Loads the data within self.data.
    """

    def __init__(self, filepath):
        """Parent initializer, then load the h5 file into the dictionary.

        :param str filepath: The path where to find the data
        """
        super().__init__(filepath)
        with h5py.File(self.filepath, 'r') as f:
            for k, v in f.items():
                self.store_element(v, self.data, k, self.skip_elements)

    def store_element(self, element, container, name, skip):
        """Stores the element, considering it as a hdf5 group or dataset.

        :param h5py.Group, h5py.Dataset element: An element of the data, either
            a Group (new dict) or a Dataset (value or array)
        :param dict container: The current dict where to store this element for
            nested architecture
        :param str name: The name for the element
        :param list skip: The list of the elements to skip if the data is too
            heavy
        """
        if type(element) is h5py.Group:
            container[name] = {}
            for k, v in element.items():
                self.store_element(v, container[name], k, skip)
        elif type(element) is h5py.Dataset:
            if name in skip:
                logger.info(f"Skipped {name} while reading {self.filepath}.")
                return
            if element.shape:
                container[name] = np.array(element)
            else:
                container[name] = element[()]
        else:
            raise TypeError(
                f"Unknown data type while reading {self.filepath}: {name}, of "
                f"type {type(element)}.")
