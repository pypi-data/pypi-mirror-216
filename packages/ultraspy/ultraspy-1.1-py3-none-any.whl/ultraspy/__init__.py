__all__ = [
    # Signal methods
    'down_mix', 'filtfilt', 'rf2iq', 'matched_filter', 'normalize',
    # Doppler methods
    'apply_wall_filter', 'spatial_smoothing', 'get_color_doppler_map',
    'get_power_doppler_map',
    # Display methods
    'to_b_mode', 'get_spectrum', 'get_doppler_colormap',
    # Post-processing methods
    'distort_dynamic',
    # Metrics
    'metrics',
    # CPU methods
    'cpu',
]

from .gpu.signal import down_mix, filtfilt, rf2iq, matched_filter, normalize
from .gpu.doppler import (apply_wall_filter, spatial_smoothing,
                          get_color_doppler_map, get_power_doppler_map)
from .gpu.display import to_b_mode, get_spectrum, get_doppler_colormap
from .gpu.post_processing import distort_dynamic
from . import metrics
from . import cpu

import sys
import logging
from .config import cfg


logging.basicConfig(format='ultraspy> %(levelname)s-%(message)s')
logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger(__name__).setLevel(logging.WARNING)
