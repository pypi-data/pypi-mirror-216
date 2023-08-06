"""Utility file for print functions, used to print the data format.
"""
import numpy as np
import scipy.io


def get_readable(values):
    """Impossible to read some data from Matlab objects here, so we replace
    them by UNK string.

    :param list, numpy.ndarray values: The values we're about to print

    :returns: The list of the values to display, or UNK if unknown
    :return type: list, numpy.ndarray
    """
    unknown_types = [scipy.io.matlab.mio5_params.mat_struct]
    return [v if (type(v) not in unknown_types) else 'UNK' for v in values]


def get_abcz(a):
    """Get 4 values to print, the first three + the last one.

    :param numpy.ndarray a: The 1D array sample to print

    :returns: The selection of data to print
    :return type: numpy.ndarray
    """
    values = np.hstack((a[0:3], a[-1]))
    unknown_types = [scipy.io.matlab.mio5_params.mat_struct]
    values = [v if (type(v) not in unknown_types) else 'UNK' for v in values]
    return values


def pretty_print_array(array):
    """Prints nicely a 1D array or a squeezable 2D array (one of the two
    dimensions is 1).

    :param numpy.ndarray array: The array to print

    :returns: The printed array inline
    :return type: str
    """
    array = np.array(get_readable(array))

    # 2D Array (1, n) or (n, 1)
    if array.ndim == 2 and np.squeeze(array).ndim == 1:
        if array.shape[0] == 1:
            return f'[{pretty_print_array(array[0])}]'
        else:
            return '[[{}] [{}] [{}] ... [{}]]'.format(*array[:, 0])

    # 1D Array
    elif array.ndim == 1:
        if array.shape[0] < 4:
            return '[' + ' '.join(['{}'.format(x) for x in array]) + ']'
        else:
            return '[{} {} {} ... {}]'.format(*get_abcz(array))

    # No instruction
    else:
        return '[...]'


def print_value(value):
    """Prints a single value based on its type (array float, whatever).

    :param int, float, str, numpy.ndarray, cupy.array value: The single value
        to print
    """
    # Check if it is an array based on the size attribute
    try:
        nb_vals = value.size
        if isinstance(value, np.ndarray):
            name_type = 'numpy.ndarray'
        else:
            name_type = 'cupy.ndarray'
            value = value.get()

        if nb_vals == 1:
            return f'({value.dtype}) -> {value}'
        else:
            return f'{value.shape} ({name_type} - {value.dtype}) ' + \
                   f'-> {pretty_print_array(value)}'

    # Else case, it is not an array
    except AttributeError:
        return str(value)


def dict_to_list_str(dictionary, indent=0):
    """Converts a dictionary into a list of strings ready to print.

    :param dict dictionary: The dictionary to print
    :param int indent: The number of spaces to put in our indentations

    :returns: The printed dictionary
    :return type: str
    """
    list_elements = []
    for k, v in dictionary.items():
        base_name = '  ' * indent + str(k)
        if isinstance(v, dict):
            list_elements.append(base_name)
            list_elements += dict_to_list_str(v, indent + 1)
        else:
            list_elements.append(base_name + ': ' + print_value(v))
    return list_elements
