"""Helpers needed for Beamformers, mainly used to deal with the available
setups (f_number, probes elements, ...). If you update this file, make sure
you also add the relevant information within  (TODO).
"""
import numpy as np


# The default values for the setup in our classes, the format is:
# { name: (default_value, type, is_an_array?), ... }
INFO = {
    'emitted_probe':     ([],   np.float32, True),
    'received_probe':    ([],   np.float32, True),
    'emitted_thetas':    ([],   np.float32, True),
    'received_thetas':   ([],   np.float32, True),
    'delays':            ([0.], np.float32, True),
    'transmissions_idx': ([0.], np.int32,   True),
    'sound_speed':       (1540, np.float32, False),
    'f_number':          (1.,   np.float32, True),
    't0':                (0.,   np.float32, False),
    'signal_duration':   (0.,   np.float32, False),
    'sampling_freq':     (0.,   np.float32, False),
    'central_freq':      (0.,   np.float32, False),
    'bandwidth':         (100., np.float32, False),
    'prf':               (1.,   np.float32, False),
}
