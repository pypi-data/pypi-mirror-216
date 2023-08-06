"""Config file. Can be called using:
from config import cfg
"""
import os
from easydict import EasyDict


__C = EasyDict()
cfg = __C

# Paths
file_dir = os.path.dirname(os.path.abspath(__file__))
__C.PATHS_RESOURCES = os.path.join(file_dir, '..', '..', 'resources')
__C.PATHS_PROBES = os.path.join(file_dir, 'probes', 'configs')

# Detect if cupy has been installed, else case, GPU mode is not available
try:
    import cupy
    __C.GPU_AVAILABLE = True
except ImportError:
    __C.GPU_AVAILABLE = False

# Environment variables
cpu_lib_env = os.getenv('ULTRASPY_CPU_LIB')
if cpu_lib_env is None:
    cpu_lib_env = 'numba'

# CPU library
__C.CPU_LIB = cpu_lib_env

# If set to True, recompile the CUDA kernels at every launch
__C.RECOMPILE_CUBIN = False
