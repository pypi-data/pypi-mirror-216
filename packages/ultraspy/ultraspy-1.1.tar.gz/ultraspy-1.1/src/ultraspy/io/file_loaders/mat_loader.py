"""Loader for .mat data, reads all the data and recovers it based on the format
of the data.
TODO: Check the way to deal the keys of the matlab objects, check on Vera data,
      there are plenty of unused data on there
"""
import scipy.io

from .file_loader import FileLoader


class MatLoader(FileLoader):
    """MatLoader class, reads the data and helps to recover. Inherit from
    FileLoader class.
    """

    def __init__(self, filepath):
        """Parent initializer, then load the mat file into the dictionary.

        :param str filepath: The path where to find the data
        """
        super().__init__(filepath)
        self.data = self.load_mat()

    def load_mat(self):
        """This function should be called instead of direct scipy.io.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects.

        :returns: The data information
        :return type: dict
        """
        data = scipy.io.loadmat(self.filepath,
                                struct_as_record=False,
                                squeeze_me=True)
        for k, v in data.items():
            if isinstance(v, scipy.io.matlab.mio5_params.mat_struct):
                data[k] = self.to_dict(v)
        return data

    def to_dict(self, mat_obj):
        """A recursive function which constructs a dictionary from nested
        mat_objects nested

        :param scipy.io.matlab.mio5_params.mat_struct mat_obj: The matlab
            object to deal with

        :returns: The converted element, either a dict of values or the values
            themselves
        """
        d = {}
        for string in mat_obj._fieldnames:
            elem = mat_obj.__dict__[string]
            if isinstance(elem, scipy.io.matlab.mio5_params.mat_struct):
                d[string] = self.to_dict(elem)
            else:
                d[string] = elem
        return d
