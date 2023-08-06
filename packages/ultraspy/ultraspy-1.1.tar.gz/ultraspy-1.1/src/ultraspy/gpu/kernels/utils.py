"""Utilities functions for the CUDA kernels.
"""
import os
import glob
import logging
from enum import Enum
import numpy as np
from pkg_resources import resource_string as read_resource

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    import cupy as cp


logger = logging.getLogger(__name__)


class GPUTypes(Enum):
    INT = np.dtype('int32')
    FLOAT = np.dtype('float32')
    COMPLEX = np.dtype('complex64')


def read_and_decode_cuda_code(file, headers=None):
    """Reads a Cuda file and adds headers if needed.

    :param str file: The name of te file
    :param list headers: List of the headers to add

    :returns: The code string
    :return type: str
    """
    headers_string = ''
    if headers is not None:
        for header in headers:
            os.path.join('headers', header)
            header_code = read_resource(__name__,
                                        os.path.join('headers', header))
            headers_string += header_code.decode() + '\n'

    cuda_code = read_resource(__name__, file)
    cuda_string = cuda_code.decode()

    return headers_string + cuda_string


def compile_bin(directory, cuda_code_file, recompile=False):
    """Compiles a Cuda code file (.cu) within a cupy.RawModule.

    :param str directory: The subdirectory where to find the cuda code (root
        directory is the `kernels/` directory)
    :param str cuda_code_file: The name of the cuda code to read
    :param bool recompile: If True, always recompile the code, slower

    :returns: The SourceModule with the compiled code
    :return type: cupy.RawModule
    """
    # Get the CUDA code
    file_path = os.path.dirname(os.path.abspath(__file__))
    local_cu_dir = os.path.join(file_path, directory)
    code_file = os.path.join(directory, cuda_code_file)

    # If recompile is set to True, we remove all the compiled files in the cupy
    # cache. This is sometimes mandatory (when changing some device functions
    # called using include)
    if recompile:
        home_dir = os.path.expanduser('~')
        files = glob.glob(os.path.join(home_dir, '.cupy/kernel_cache/*'))
        for f in files:
            os.remove(f)

    # Compilation of the .cu code, with the required list of headers, open to
    # call all the other .cu codes within `local_cu_dir`
    code = read_and_decode_cuda_code(code_file, headers=['cupy_header.cu'])
    return cp.RawModule(code=code,
                        options=('-std=c++11', f'-I {local_cu_dir}',))


def call_function_given_type(all_functions_dict):
    """Returns the proper kernel given the type of the first argument. These
    kernels are all independent, but are mingled here for simplicity.

    :param dict all_functions_dict: A directory with the different kernels for
        all the type of this function. The key is a TYPE_ENUM, the value the
        cupy kernel

    :returns: The proper kernel
    :return type: cupy.RawKernel
    """
    def caller(grid, block, args, shared_mem=0):
        data = args[0]
        if data.dtype not in all_functions_dict.keys():
            raise TypeError("This {} type is not supported for this kernel".
                            format(GPUTypes(data.dtype)))
        k = all_functions_dict[data.dtype]
        return k(grid, block, args, shared_mem=shared_mem)

    return caller
