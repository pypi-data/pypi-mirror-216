"""Utilities for GPU manipulations.
"""
import logging

from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    import cupy as cp


logger = logging.getLogger(__name__)


def send_to_gpu(data, dtype):
    """Send the data on GPU.

    :param numpy.ndarray data: The data array to send to GPU
    :param type dtype: The data type

    :returns: The GPU array
    :return type: cupy.array
    """
    return cp.asarray(data.astype(dtype))


def initialize_empty(data_shape, dtype):
    """Initialized an empty array on GPU based on the library currently used.

    :param tuple data_shape: The shape of the data
    :param type dtype: The data type

    :returns: The GPU array
    :return type: cupy.array
    """
    return cp.empty(data_shape, dtype)


def set_values(dst, src):
    """Replaces the values within dst by those on src.

    :param cupy.array dst: The array to replace
    :param cupy.array src: The array with the values
    """
    cp.copyto(dst, src)


def swap_axes(d_data, axis_1, axis_2):
    """Interchanges two axes of an array.

    :param cupy.array d_data: The input array
    :param int axis_1: The first axis
    :param int axis_2: The second axis
    """
    return cp.swapaxes(d_data, axis_1, axis_2).copy()


def move_axis(d_data, src_axis, dst_axis):
    """Moves an axis from a source dimension to a destination dimension.

    :param cupy.array d_data: The input array
    :param int src_axis: The source axis
    :param int dst_axis: The destination axis
    """
    return cp.moveaxis(d_data, src_axis, dst_axis).copy()


def reshape(d_data, shape):
    """Reshapes the d_data array to the new shape.

    :param cupy.array d_data: The input array
    :param tuple shape: The final shape
    """
    return cp.reshape(d_data, shape).copy()


def squeeze_axes(d_data, axes):
    """Squeezes the data along the requested axes.

    :param cupy.array d_data: The input array
    :param tuple axes: The axes where to squeeze the data
    """
    return cp.squeeze(d_data, axis=axes).copy()


def all_equal(d_array_1, d_array_2):
    """Returns True if both arrays are all close.

    :param cupy.array d_array_1: The first array, on device
    :param cupy.array d_array_2: The second array, on device
    """
    if d_array_1.shape == d_array_2.shape:
        return cp.allclose(d_array_1, d_array_2).item()
    return False


def compute_flat_grid_size(nb_points, max_threads=512):
    """Returns the appropriate grid / block size given the number of points we
    want to compute in a kernel.

    :param int nb_points: The number of points we'll have to compute in our
        kernel
    :param int max_threads: The maximum number of threads to use at the same
        time

    :returns: The grid / block architectures
    :return type: tuple
    """
    b_dim = (max_threads, 1, 1)
    dx, mx = divmod(nb_points, b_dim[0])
    g_dim = ((dx + (mx > 0)), 1, 1)
    return g_dim, b_dim
