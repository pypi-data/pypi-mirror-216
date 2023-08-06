"""Matplotlib utilities, it is mainly here to improve the visualization of our
metrics methods. Doesn't necessary need to be tested as it is only
visualization.
"""
import numpy as np
from matplotlib.patches import Rectangle


def add_rectangle_patch(plt_axis, data, bounds, text, offset=10):
    """Adds a rectangle on an axis, flexible to the data itself (its min and
    max) and given the bounds of the left / right sides.

    :param matplotlib.pyplot.Axes plt_axis: The axis where to add the rectangle
    :param numpy.ndarray data: The signal to catch, to have the min / max
        values and draw a better rectangle
    :param tuple bounds: The left and right indices for the rectangle
    :param str text: The text to display near the rectangle
    :param int offset: The space to leave between the min / max of the data and
        the rectangle, for nicer visualization (default to 10)
    """
    y_axis = plt_axis.get_ylim()
    offset *= max(y_axis) / 100
    x1, x2 = bounds
    y1 = max(np.min(data) - offset, y_axis[0])
    y2 = min(np.max(data) + offset, y_axis[1])
    plt_axis.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=None))
    plt_axis.text(x1 + (x2 - x1) // 2, y1 + offset,
                  text, horizontalalignment='center')
