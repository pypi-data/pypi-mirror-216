.. _common_methods:

`ultraspy` core methods
=======================
The main methods in `ultraspy` are defined both in GPU and in CPU, and are
stored within the dedicated repositories :code:`gpu/` and :code:`cpu/`. The GPU
version are highlighted, so those can be called directly from the `ultraspy`
module. Their CPU alternatives, however, need to be called using the
`ultraspy.cpu` module. For example:

.. code-block:: python

    import ultraspy as us

    # Call the GPU method, input / output are on the GPU device
    d_out = us.some_method(d_input, ...)

    # Call the CPU alternative
    out = us.cpu.some_method(input, ...)


Signal-related methods
----------------------
The detailed description can be found in the API reference (TODO).

* :code:`down_mix`: Down-mixing operation, performs a phase rotation on our
  data to move the spectrum around 0 Hz (involving the returned signal to be
  complex).

* :code:`filtfilt`: Butterworth filtfilt, greatly inspired by Matlab's filtfilt
  version, zero-phase forward and reverse digital filtering.

* :code:`rf2iq`: Converts raw RFs data signals into I/Qs (In-Phase Quadrature).
  Consists in a down-mixing operation (centers the spectrum at 0Hz), followed
  by a low-pass filter to keep only the newly centered at 0 spectrum (remove
  the old negative component).

* :code:`matched_filter`: Applies a matched filter to our data, given a
  reference signal which is supposed to match.

* :code:`normalize`: Simply normalizes a signal to values between -1 and 1.


Doppler-related methods
-----------------------
The detailed description can be found in the API reference (TODO).

* :code:`apply_wall_filter`: Applies a clutter filter along slow time. The
  clutter type can be either 'mean' (subtract the mean of the data), 'poly'
  (applies a polynomial filter) or 'hp_filter' (applies a high-pass butterworth
  filter).

* :code:`spatial_smoothing`: Performs a spatial smoothing on data, using a
  given window function to compute the squared convolution kernel (either
  hamming or median).

* :code:`get_color_doppler_map`: Computes the color doppler map, which is using
  the correlation of our data along slow time, which are then converted to
  doppler velocity using the Doppler formula. It also can perform a spatial
  smoothing of a given number of pixels.

* :code:`get_power_doppler_map`: Computes the power doppler map, which is using
  the mean of squared values along slow time. The result is then returned in
  dB. It can also perform a spatial smoothing of a given number of pixels.


Displaying methods
------------------
The detailed description can be found in the API reference (TODO).

* :code:`to_b_mode`: Computes the B-Mode of our beamformed data. Simply returns
  20 * log10(data).

* :code:`get_spectrum`: Returns the spectrum of a data signal.

* :code:`get_doppler_colormap`: Returns a color map proposition for Doppler,
  based on typical echographs, from blue (flow going away from the probe), to
  red (going toward to).


Post-processing methods
-----------------------
The detailed description can be found in the API reference (TODO).

* :code:`distort_dynamic`: Post-processing method to distort the dynamic of a
  B-Mode image (already in dB). This is applying a mathematical function,
  either curved or sigmoid to distort the values of the image.


Metrics methods
---------------
The detailed description can be found in the API reference (TODO).

* :code:`metrics.signal_noise_ratio`: Returns the Signal to Noise ratio of the
  sample, based on the location of both the pulse and the noise.

* :code:`metrics.get_full_width_at_half_maximum`: Returns the Full-Width at
  Half Maximum of a signal, given a focus index. It is basically the width of
  the focused lobe at -6dB.

* :code:`metrics.get_peak_side_lobe`: Returns the Peak Side Lobe of a signal,
  given a focus index. It is basically the difference in dB between the focused
  lobe and its closest neighbor.

* :code:`metrics.get_contrat_noise_ratio`: Returns the Contrast to Noise ratio
  of the data, using two masks, one for the position of the signal, the other
  one for the noise.
