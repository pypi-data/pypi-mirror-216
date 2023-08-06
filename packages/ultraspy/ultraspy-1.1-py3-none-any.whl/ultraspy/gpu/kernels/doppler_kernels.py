"""Factory for the doppler kernels. Reads the cuda code and extract their
functions so they can be called by the library.
Note: This should not be accessible by users

The following kernels can be imported from the factory:
- k_mean_wall_filter: The 'mean' wall filter, which simply removes the mean of
                      data along the slow time (last dimension). Receives a 2d
                      array
- k_mean_wall_filter_first_axis: Same as k_mean_wall_filter, but works on first
                                 dimension
- k_poly_wall_filter: The polynomial wall filter, which removes the first n
                      degrees of a polynomial regression to the data along the
                      slow time (last dimension) along the slow time (last
                      dim). Receives a 2d array
- k_poly_wall_filter_first_axis: Same as k_poly_wall_filter, but works on first
                                  dimension
- k_correlation_matrix: The kernel used to compute the correlation matrix for
                        color doppler, considering the slow time is in the last
                        axis
- k_color_map: The kernel used to compute the color doppler map from the
               correlation matrix
- k_power_map: The kernel used to compute the power doppler map. In fact it is
               doing the sum of squared element along an axis.. the to DB
               process is not done here, so it might worth considering it as an
               operator...?
"""
from ultraspy.config import cfg

from .utils import (compile_bin,
                    call_function_given_type,
                    GPUTypes)


# All the operators' kernel codes can be found within the doppler directory
DIR = 'doppler'
RECOMPILE = cfg.RECOMPILE_CUBIN


# Re-compile the code if requested
mod_mean_wall_filter = compile_bin(DIR, 'mean_wall_filter.cu', RECOMPILE)
mod_poly_wall_filter = compile_bin(DIR, 'poly_wall_filter.cu', RECOMPILE)
mod_correlation_matrix = compile_bin(DIR, 'correlation_matrix.cu', RECOMPILE)
mod_color_map = compile_bin(DIR, 'color_map.cu', RECOMPILE)
mod_power_map = compile_bin(DIR, 'power_map.cu', RECOMPILE)

# Local kernels, based on the type of the first argument (often the array we
# want to perform operation on)
_k_mean_wall_filter_types = {
    GPUTypes.COMPLEX.value: mod_mean_wall_filter.get_function(
        'mean_wall_filter'),
}
_k_mean_wall_filter_first_axis_types = {
    GPUTypes.COMPLEX.value: mod_mean_wall_filter.get_function(
        'mean_wall_filter_first_axis'),
}
_k_poly_wall_filter_types = {
    GPUTypes.COMPLEX.value: mod_poly_wall_filter.get_function(
        'poly_wall_filter'),
}
_k_poly_wall_filter_first_axis_types = {
    GPUTypes.COMPLEX.value: mod_poly_wall_filter.get_function(
        'poly_wall_filter_first_axis'),
}
_k_correlation_matrix_types = {
    GPUTypes.COMPLEX.value: mod_correlation_matrix.get_function(
        'correlation_matrix'),
}
_k_color_map_types = {
    GPUTypes.COMPLEX.value: mod_color_map.get_function('color_map'),
}
_k_power_map_types = {
    GPUTypes.COMPLEX.value: mod_power_map.get_function('power_map'),
}

# Kernels
k_mean_wall_filter = call_function_given_type(_k_mean_wall_filter_types)
k_mean_wall_filter_first_axis = call_function_given_type(
    _k_mean_wall_filter_first_axis_types)
k_poly_wall_filter = call_function_given_type(_k_poly_wall_filter_types)
k_poly_wall_filter_first_axis = call_function_given_type(
    _k_poly_wall_filter_first_axis_types)
k_correlation_matrix = call_function_given_type(_k_correlation_matrix_types)
k_color_map = call_function_given_type(_k_color_map_types)
k_power_map = call_function_given_type(_k_power_map_types)
