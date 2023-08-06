"""Helpers needed for Beamformers, mainly used to deal with the available
options (apodization, interpolation, ...). If you update this file, make sure
you also add the relevant information within the (TODO).
"""
import numpy as np
from enum import Enum


# The default values for the options in our classes, the format is:
# { name: (default_value, type, is_an_array?), ... }
INFO = {
    'interpolation':        ('linear',    np.int32,   False),
    'reduction':            ('sum',       np.int32,   False),
    'rx_apodization':       ('boxcar',    np.int32,   False),
    'rx_apodization_alpha': (0.1,         np.float32, False),
    'compound':             (True,        np.int32,   False),
    'reduce':               (True,        np.int32,   False),
    'fix_t0':               (True,        np.int32,   False),
    'emitted_aperture':     (True,        np.int32,   False),
}


class Interpolation(Enum):
    NONE = 0
    LINEAR = 1
    QUADRATIC = 2
    CUBIC = 3


class Apodization(Enum):
    BOXCAR = 0
    TUKEY = 1


class Reduction(Enum):
    SUM = 0
    MEAN = 1


class Compound(Enum):
    FALSE = 0
    TRUE = 1


class Reduce(Enum):
    FALSE = 0
    TRUE = 1


class FixT0(Enum):
    FALSE = 0
    TRUE = 1


class EmittedAperture(Enum):
    FALSE = 0
    TRUE = 1


def factory(option, value):
    """Factory to return the proper enum element given a string value, for ease
    of use.

    :param str option: The name of the parameter
    :param str, float value: The value to look for

    :returns: The enum element (unique integer to read in cuda kernels)
    :return type: enum, str, float
    """
    if type(value) == INFO[option][1]:
        return value

    if option == 'interpolation':
        return Interpolation[value.upper()].value
    elif option == 'reduction':
        return Reduction[value.upper()].value
    elif option == 'rx_apodization':
        return Apodization[value.upper()].value
    elif option == 'compound':
        return Compound[str(value).upper()].value
    elif option == 'reduce':
        return Reduce[str(value).upper()].value
    elif option == 'fix_t0':
        return FixT0[str(value).upper()].value
    elif option == 'emitted_aperture':
        return EmittedAperture[str(value).upper()].value
    else:
        return value
