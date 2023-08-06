"""Factory for the operators kernels. Reads the cuda code and extract their
functions, so they can be called by the library.
Note: This should not be accessible by users

The following kernels can be imported from the factory:
- k_by2: The operator by 2, takes an array and multiply every element by 2
- k_divide_by: The operator divided by, to divide every element of the array by
               a float value
- k_flip: The operator flip, takes a 2d array and flip it along first dimension
- k_flip_within: Same as k_flip, but not inplace
- k_flip_old: Same as k_flip, but along last dimension somehow, for filtfilt
- k_flip_within_old: Same as k_flip_within, but along last dimension somehow,
                     for filtfilt
- k_get_modulo: Returns the modulo of a complex array
- k_power_to_db: Exposes every elements to dB by 10 * log10(data)
- k_to_db: Exposes every elements to dB by 20 * log10(data)
- k_convolve1d: Returns the convolved last axis of our data given a kernel
- k_convolve2d: Returns the convolved 2D data using a given kernel
- k_median_convolve: Returns the median filter of a data array
- k_max: Returns the maximum of an array
"""
from ultraspy.config import cfg

from .utils import (compile_bin,
                    call_function_given_type,
                    GPUTypes)


# All the operators' kernel codes can be found within the operators directory
DIR = 'operators'
RECOMPILE = cfg.RECOMPILE_CUBIN

# Re-compile the code if requested
mod_by2 = compile_bin(DIR, 'by2.cu', RECOMPILE)
mod_divide_by = compile_bin(DIR, 'divide_by.cu', RECOMPILE)
mod_flip = compile_bin(DIR, 'flip.cu', RECOMPILE)
mod_get_modulo = compile_bin(DIR, 'get_modulo.cu', RECOMPILE)
mod_to_db = compile_bin(DIR, 'to_db.cu', RECOMPILE)
mod_convolve = compile_bin(DIR, 'convolve.cu', RECOMPILE)
mod_median_filter = compile_bin(DIR, 'median_filter.cu', RECOMPILE)

# Local kernels, based on the type of the first argument (often the array we
# want to perform operation on)
_k_by2_types = {
    GPUTypes.INT.value: mod_by2.get_function('by2_int'),
    GPUTypes.FLOAT.value: mod_by2.get_function('by2_float'),
    GPUTypes.COMPLEX.value: mod_by2.get_function('by2_complex'),
}
_k_divide_by_types = {
    GPUTypes.FLOAT.value: mod_divide_by.get_function('divide_by_float'),
    GPUTypes.COMPLEX.value: mod_divide_by.get_function('divide_by_complex'),
}
_k_flip_types = {
    GPUTypes.INT.value: mod_flip.get_function('flip_int'),
    GPUTypes.FLOAT.value: mod_flip.get_function('flip_float'),
    GPUTypes.COMPLEX.value: mod_flip.get_function('flip_complex'),
}
_k_flip_within_types = {
    GPUTypes.INT.value: mod_flip.get_function('flip_within_int'),
    GPUTypes.FLOAT.value: mod_flip.get_function('flip_within_float'),
    GPUTypes.COMPLEX.value: mod_flip.get_function('flip_within_complex'),
}
_k_flip_old_types = {
    GPUTypes.COMPLEX.value: mod_flip.get_function('flip_old_complex'),
}
_k_flip_within_old_types = {
    GPUTypes.COMPLEX.value: mod_flip.get_function('flip_within_old_complex'),
}
_k_get_modulo_types = {
    GPUTypes.COMPLEX.value: mod_get_modulo.get_function('get_modulo'),
}
_k_to_db_types = {
    GPUTypes.FLOAT.value: mod_to_db.get_function('to_db_float'),
}
_k_power_to_db_types = {
    GPUTypes.FLOAT.value: mod_to_db.get_function('power_to_db_float'),
}
_k_convolve1d_types = {
    GPUTypes.FLOAT.value: mod_convolve.get_function('convolve1d_float'),
    GPUTypes.COMPLEX.value: mod_convolve.get_function('convolve1d_complex'),
}
_k_convolve2d_types = {
    GPUTypes.FLOAT.value: mod_convolve.get_function('convolve2d_float'),
    GPUTypes.COMPLEX.value: mod_convolve.get_function('convolve2d_complex'),
}
_k_median_filter_types = {
    GPUTypes.FLOAT.value: mod_median_filter.get_function('median_filter_float'),
    GPUTypes.COMPLEX.value: mod_median_filter.get_function(
        'median_filter_complex'),
}

# Kernels
k_by2 = call_function_given_type(_k_by2_types)
k_divide_by = call_function_given_type(_k_divide_by_types)
k_flip = call_function_given_type(_k_flip_types)
k_flip_within = call_function_given_type(_k_flip_within_types)
k_flip_old = call_function_given_type(_k_flip_old_types)
k_flip_within_old = call_function_given_type(_k_flip_within_old_types)
k_get_modulo = call_function_given_type(_k_get_modulo_types)
k_to_db = call_function_given_type(_k_to_db_types)
k_power_to_db = call_function_given_type(_k_power_to_db_types)
k_convolve1d = call_function_given_type(_k_convolve1d_types)
k_convolve2d = call_function_given_type(_k_convolve2d_types)
k_median_filter = call_function_given_type(_k_median_filter_types)

# Min / Max are already implemented reduction kernels, use them
# TODO: Should be removed now
k_max = lambda d: d.max().get().item()
