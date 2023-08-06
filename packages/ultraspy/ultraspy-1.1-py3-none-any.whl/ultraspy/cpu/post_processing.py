"""Methods for post-processing the data.
"""
import numpy as np


def distort_dynamic(b_mode, method, params, dynamic, norm=False):
    """Post-processing method to distort the dynamic of a B-Mode image (already
    in dB). This is applying a mathematical function, either curved or sigmoid
    to distort the values of the image in order to distort the dynamic. Note
    that this will clip the data between `dynamic` and 0.

    :param numpy.ndarray b_mode: the original B-Mode image
    :param str method: the name of the function to apply, either 'curve' or
        'sigmoid'
    :param dict params: the parameters of the function:

        - if 'curved', expects the 'curve' argument (]0, 1[)
        - if 'sigmoid', expects the 'steep' (]0, 2]) and the 'offset' ([0, 5])

    :param int dynamic: the dynamic for display, negative integer
    :param bool norm: if set to True, the function is normalized. Given the
        parameters provided, the functions might not be filling the whole range
        between 0 and 1, meaning that the distorted values won't always have 1
        as maximum value. Normalization 'fixes' this

    :returns: The distorted B-Mode image
    :return type: numpy.ndarray
    """
    if method not in ['curved', 'sigmoid']:
        raise AttributeError(
            f"Unknown distortion type '{method}', pick either 'curved' or "
            "'sigmoid'.")

    # Check general parameters
    if method == 'curved':
        assert 'curve' in params, "Missing 'curve' argument."
        assert 0 < params['curve'] < 1, "'curve' should be between ]0, 1[."
    if method == 'sigmoid':
        assert 'steep' in params, "Missing 'steep' argument."
        assert 'offset' in params, "Missing 'offset' argument."
        assert 0 < params['steep'] <= 2, "'steep' should be between ]0, 2]."
        assert 0 <= params['offset'] <= 5, "'offset' should be between [0, 5]."

    # Normalize and clip the data to apply the distortion
    b_mode = np.clip(-(b_mode / dynamic) + 1, 0, 1)
    ref_max = np.max(b_mode)

    # Distort the data with the chosen method
    if method == 'curved':
        b_mode = np.power(b_mode, (1 / params['curve'] - 1))
    elif method == 'sigmoid':
        stretch = 5
        b_mode = b_mode * 2 * stretch - stretch
        b_mode = 1 / (1 + np.exp(-b_mode / params['steep'] + params['offset']))

    # If needed, we normalize before restoring the dynamic
    if norm:
        b_mode -= np.min(b_mode)
        b_mode /= np.max(b_mode)
        b_mode *= ref_max

    # Restore the dynamic
    b_mode = (1 - b_mode) * dynamic

    return b_mode
