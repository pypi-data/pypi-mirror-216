"""Factory to get a file loader based on its extension.
"""
import os

from .h5_loader import H5Loader
from .mat_loader import MatLoader
from .rff256_loader import Rff256Loader


def get_file_loader(data_file):
    """Factory to read the dedicated FileLoader class based on the file
    extension. Note that the .mat files we are using are supported by the h5
    loader library, since they've been computed using Matlab version >= 7.3.
    If the version used is below, you will have to use the scipy loadmat
    function.

    :param str data_file: The path where to find the data

    :returns: The FileLoader class with the raw info from the data
    :return type: H5Loader, MatLoader, Rff256Loader
    """
    extension = os.path.splitext(data_file)[1]
    if extension in ['.hdf5', '.h5']:
        return H5Loader(data_file)
    elif extension == '.mat':
        try:
            return MatLoader(data_file)
        except NotImplementedError:
            return H5Loader(data_file)
    if extension in ['.rff256', '.rfb256']:
        return Rff256Loader(data_file)
    else:
        raise AttributeError(f"Can't read {data_file}. Unknown extension.")
