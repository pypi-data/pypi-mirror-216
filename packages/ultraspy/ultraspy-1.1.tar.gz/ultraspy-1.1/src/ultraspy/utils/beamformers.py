"""Helpers for beamformers.
"""


def get_axes_to_reduce(compound, reduce):
    """Simple helpers to get the axes to reduce given the selected options.

    :param int, bool compound: If True, compound the data (along the
        transmissions, first dim)
    :param int, bool reduce: If True, reduce the data (along the probe
        elements, second dim)

    :returns: The tuple of the axes to reduce.
    :return type: tuple
    """
    axes = []
    if bool(compound):
        axes.append(0)
    if bool(reduce):
        axes.append(1)
    return tuple(axes)
