"""Factory for the beamformers kernels. Reads the cuda code and extract their
functions, so they can be called by the library.
Note: This should not be accessible by users

The following kernels can be imported from the factory:
- k_das: The DAS kernel, which can be either performed on RFs (if data is of
         type np.float32) or I/Qs (np.complex64).
"""
from ultraspy.config import cfg

from .utils import (compile_bin,
                    call_function_given_type,
                    GPUTypes)


# All the operators' kernel codes can be found within the doppler directory
DIR = 'beamformers'
RECOMPILE = cfg.RECOMPILE_CUBIN


# Re-compile the code if requested
mod_das = compile_bin(DIR, 'das.cu', RECOMPILE)
mod_fdmas = compile_bin(DIR, 'fdmas.cu', RECOMPILE)
mod_pdas = compile_bin(DIR, 'pdas.cu', RECOMPILE)


# Local kernels, based on the type of the first argument (often the array we
# want to perform operation on)
_k_das_types = {
    GPUTypes.FLOAT.value: mod_das.get_function('das_float'),
    GPUTypes.COMPLEX.value: mod_das.get_function('das_complex'),
}
_k_packet_das_types = {
    GPUTypes.FLOAT.value: mod_das.get_function('packet_das_float'),
    GPUTypes.COMPLEX.value: mod_das.get_function('packet_das_complex'),
}
_k_fdmas_types = {
    GPUTypes.FLOAT.value: mod_fdmas.get_function('dmas_float'),
    GPUTypes.COMPLEX.value: mod_fdmas.get_function('dmas_complex'),
}
_k_packet_fdmas_types = {
    GPUTypes.FLOAT.value: mod_fdmas.get_function('packet_dmas_float'),
    GPUTypes.COMPLEX.value: mod_fdmas.get_function('packet_dmas_complex'),
}
_k_pdas_types = {
    GPUTypes.FLOAT.value: mod_pdas.get_function('pdas_float'),
    GPUTypes.COMPLEX.value: mod_pdas.get_function('pdas_complex'),
}
_k_packet_pdas_types = {
    GPUTypes.FLOAT.value: mod_pdas.get_function('packet_pdas_float'),
    GPUTypes.COMPLEX.value: mod_pdas.get_function('packet_pdas_complex'),
}


# Kernels
k_das = call_function_given_type(_k_das_types)
k_packet_das = call_function_given_type(_k_packet_das_types)
k_fdmas = call_function_given_type(_k_fdmas_types)
k_packet_fdmas = call_function_given_type(_k_packet_fdmas_types)
k_pdas = call_function_given_type(_k_pdas_types)
k_packet_pdas = call_function_given_type(_k_packet_pdas_types)
