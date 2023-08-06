"""Factory for the signal kernels. Reads the cuda code and extract their
functions so they can be called by the library.
Note: This should not be accessible by users

The following kernels can be imported from the factory:
- k_down_mix: Used to mix a signal with a complex sinusoid signal
- k_init_filter: TODO: Complete
- k_init_start_sig: TODO: Complete
- k_filter0: TODO: Complete
- k_init_end_sig: TODO: Complete

TODO: Should test the filtfilt with floats
"""
from ultraspy.config import cfg

from .utils import (compile_bin,
                    call_function_given_type,
                    GPUTypes)

# All the operators' kernel codes can be found within the doppler directory
DIR = 'signal'
RECOMPILE = cfg.RECOMPILE_CUBIN


# Re-compile the code if requested
mod_down_mix = compile_bin(DIR, 'down_mix.cu', RECOMPILE)
mod_init_filter = compile_bin(DIR, 'init_filter.cu', RECOMPILE)
mod_init_start_sig = compile_bin(DIR, 'init_start_sig.cu', RECOMPILE)
mod_filter0 = compile_bin(DIR, 'filter0.cu', RECOMPILE)
mod_init_end_sig = compile_bin(DIR, 'init_end_sig.cu', RECOMPILE)

# Local kernels, based on the type of the first argument (often the array we
# want to perform operation on)
_k_down_mix_types = {
    GPUTypes.COMPLEX.value: mod_down_mix.get_function('down_mix'),
}
_k_init_filter_types = {
    GPUTypes.FLOAT.value: mod_init_filter.get_function('init_filter_float'),
    GPUTypes.COMPLEX.value: mod_init_filter.get_function('init_filter_complex'),
}
_k_init_start_sig_types = {
    GPUTypes.FLOAT.value: mod_init_start_sig.get_function(
        'init_start_sig_float'),
    GPUTypes.COMPLEX.value: mod_init_start_sig.get_function(
        'init_start_sig_complex'),
}
_k_filter0_types = {
    GPUTypes.FLOAT.value: mod_filter0.get_function('filter0_float'),
    GPUTypes.COMPLEX.value: mod_filter0.get_function('filter0_complex'),
}
_k_init_end_sig_types = {
    GPUTypes.FLOAT.value: mod_init_end_sig.get_function('init_end_sig_float'),
    GPUTypes.COMPLEX.value: mod_init_end_sig.get_function(
        'init_end_sig_complex'),
}

# Kernels
k_down_mix = call_function_given_type(_k_down_mix_types)
k_init_filter = call_function_given_type(_k_init_filter_types)
k_init_start_sig = call_function_given_type(_k_init_start_sig_types)
k_filter0 = call_function_given_type(_k_filter0_types)
k_init_end_sig = call_function_given_type(_k_init_end_sig_types)
