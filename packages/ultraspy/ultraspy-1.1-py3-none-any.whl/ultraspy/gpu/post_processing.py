"""Methods for post-processing the data.
"""
from ultraspy.config import cfg
if cfg.GPU_AVAILABLE:
    import cupy as cp

    from ultraspy.gpu import gpu_utils


def distort_dynamic(d_b_mode, method_type, params, dynamic, norm=False,
                    inplace=True):
    """Post-processing method to distort the dynamic of a B-Mode image (already
    in dB). This is applying a mathematical function, either curved or sigmoid
    to distort the values of the image in order to distort the dynamic. Note
    that this will clip the data between `dynamic` and 0.

    :param cupy.array d_b_mode: the original B-Mode image, on GPU
    :param str method_type: the name of the function to apply, either 'curve'
        or 'sigmoid'
    :param dict params: the parameters of the function:
        - if 'curved', expects the 'curve' argument (]0, 1[)
        - if 'sigmoid', expects the 'steep' (]0, 2]) and the 'offset' ([0, 5])
    :param int dynamic: the dynamic for display, negative integer
    :param bool norm: if set to True, the function is normed
    :param bool inplace: If set to True, d_data is directly modified. Else
        case, a new slot is allocated on GPU, and the result is returned while
        d_data is kept

    :returns: The distorted B-Mode image
    :return type: numpy.ndarray
    """
    if not inplace:
        d_new = gpu_utils.initialize_empty(d_b_mode.shape, d_b_mode.dtype)
        gpu_utils.set_values(d_new, d_b_mode)
        distort_dynamic(d_new, method_type, params, dynamic, norm)
        return d_new

    assert method_type in ['curved', 'sigmoid'], 'Unknown function.'
    if method_type == 'curved':
        assert 'curve' in params, "Missing 'curve' argument."
        assert 0 < params['curve'] < 1, "'curve' should be between ]0, 1[."
    if method_type == 'sigmoid':
        assert 'steep' in params, "Missing 'steep' argument."
        assert 'offset' in params, "Missing 'offset' argument."
        assert 0 < params['steep'] <= 2, "'steep' should be between ]0, 2]."
        assert 0 <= params['offset'] <= 5, "'offset' should be between [0, 5]."

    d_b_mode /= dynamic
    d_b_mode = cp.clip(-d_b_mode + 1, 0, 1)
    ref_max = cp.max(d_b_mode)

    if method_type == 'curved':
        curve = params['curve']
        d_b_mode = cp.power(d_b_mode, (1 / curve) - 1)
    elif method_type == 'sigmoid':
        stretch = 5
        steep = params['steep']
        offset = params['offset']
        d_b_mode = d_b_mode * 2 * stretch - stretch
        d_b_mode = 1 / (1 + cp.exp(-d_b_mode / steep + offset))

    if norm:
        d_b_mode -= cp.min(d_b_mode)
        d_b_mode /= cp.max(d_b_mode)
        d_b_mode *= ref_max

    d_b_mode = (1 - d_b_mode) * dynamic

    return d_b_mode
