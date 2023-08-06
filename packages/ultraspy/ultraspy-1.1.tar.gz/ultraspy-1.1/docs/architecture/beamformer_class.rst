.. _beamformer_class:

The Beamformer class
====================
When instantiating a beamformer class with the settings from the Reader, we
expect to store values for all the :code:`beamformer.setups` and the
:code:`beamformer.options`.

Beamformer setups
-----------------
The setups are here to store the main information. The list of the setups is
defined within `beamformers/setups.py`, but these are:

.. table::
    :class: wy-table-responsive

    +---------------------+------------+---------+--------------+
    | Setup name          | Type       | Default | Description  |
    +=====================+============+=========+==============+
    | `emitted_probe`     | array_like |         | |probe_txt|  |
    | `received_probe`    |            |         |              |
    +---------------------+------------+---------+--------------+
    | `delays`            | array_like |         | |delays_txt| |
    +---------------------+------------+---------+--------------+
    | `transmissions_idx` | array_like |         | |trs_txt|    |
    +---------------------+------------+---------+--------------+
    | `sound_speed`       | float      | 1540.   | |sos_txt|    |
    +---------------------+------------+---------+--------------+
    | `f_number`          | float      | 1.      | |fnb_txt|    |
    +---------------------+------------+---------+--------------+
    | `t0`                | float      | 0.      | |t0_txt|     |
    +---------------------+------------+---------+--------------+
    | `sampling_freq`     | float      |         | |fs_txt|     |
    +---------------------+------------+---------+--------------+
    | `central_freq`      | float      |         | |f0_txt|     |
    +---------------------+------------+---------+--------------+
    | `signal_duration`   | float      | 0.      | |sigdur_txt| |
    +---------------------+------------+---------+--------------+
    | `bandwidth`         | float      | 100.    | |band_txt|   |
    +---------------------+------------+---------+--------------+
    | `prf`               | float      | 1.      | |prf_txt|    |
    +---------------------+------------+---------+--------------+
    | `emitted_thetas`    | array_like | [0.]    | |thetas_txt| |
    | `received_thetas`   |            |         |              |
    +---------------------+------------+---------+--------------+

.. |probe_txt| replace:: These are the probes used to acquire the data, they
    both have the shape (3, nb_transmissions, nb_elements). The first dimension
    is the x, y and z positions of the elements, and, for each transmissions,
    the concerned elements. This configuration allows to have distinct emission
    and reception probe (which is useful for STA for example). Stored in m.
.. |delays_txt| replace:: The acquisition delays for each cycle for each
    element. If we are sending tilted plane waves, the delays are stored here
    (in s).
.. |trs_txt| replace:: The indices for the transmissions, as integers, if you
    don't want to perform the beamforming on all transmissions (single plane
    wave vs full compounded for example).
.. |sos_txt| replace:: The speed of sound used to compute the delays, or simply
    an estimation of the medium sound of speed if there's no delays (in m/s).
.. |fnb_txt| replace:: The f-number to use for the beamforming.
.. |t0_txt| replace:: The initial time to add to the transmission times (in s).
.. |fs_txt| replace:: The sampling frequency of the acquisition system (in Hz).
.. |f0_txt| replace:: The central frequency of the probe (in Hz).
.. |sigdur_txt| replace:: The duration of the emitted signal, it is used to
    adjust the original t0 to the center of the emission pulse.
.. |band_txt| replace:: The bandwidth of the probe, in %.
.. |prf_txt| replace:: The Pulse Repetition Frequency (in Hz).
.. |thetas_txt| replace:: For convex probes, this indicates the thetas of the
    probe for each emitted / received probe elements.


Each of these setups can be updated at any time using:

.. code-block:: python
    :linenos:

    beamformer.update_setup('name_of_setup', value)


Beamformer options
------------------
The options are here to define the beamforming options, not all of them are
implemented in all the beamformers though:

.. table::
    :class: wy-table-responsive

    +------------------------+----------+----------+-----------------+
    | Option name            | Type     | Default  | Description     |
    +========================+==========+==========+=================+
    | `interpolation`        | int str  | 'linear' | |interp_txt|    |
    +------------------------+----------+----------+-----------------+
    | `reduction`            | int str  | 'sum'    | |reduction_txt| |
    +------------------------+----------+----------+-----------------+
    | `rx_apodization`       | int str  | 'boxcar' | |rx1_txt|       |
    +------------------------+----------+----------+-----------------+
    | `rx_apodization_alpha` | float    | 0.1      | |rx2_txt|       |
    +------------------------+----------+----------+-----------------+
    | `compound`             | int bool | True     | |compound_txt|  |
    +------------------------+----------+----------+-----------------+
    | `reduce`               | int bool | True     | |reduce_txt|    |
    +------------------------+----------+----------+-----------------+
    | `fix_t0`               | int bool | True     | |ft0_txt|       |
    +------------------------+----------+----------+-----------------+
    | `emitted_aperture`     | int bool | True     | |ea_txt|        |
    +------------------------+----------+----------+-----------------+

.. |interp_txt| replace:: The interpolation method to use (can be either
    'none', 'linear', 'quadratic' or 'cubic'). The latter two are only
    implemented in Numpy (CPU).
.. |reduction_txt| replace:: The reduction method, either 'sum' or 'mean'. This
    is defining the way we are reducing the delays at the end of the
    beamforming process.
.. |rx1_txt| replace:: The reception apodization method, either 'boxcar' or
    'tukey', only 'boxcar' is supported by Numpy.
.. |rx2_txt| replace:: The coefficient for the apodization method.
.. |compound_txt| replace:: If set to True, we compound the data along the
    transmission axis. Can be combined with reduce.
.. |reduce_txt| replace:: If set to True, we reduce the data along the received
    probe elements. Can be combined with compound. Only supported for DAS
    beamformer.
.. |ft0_txt| replace:: If set to True, the t0 is automatically set to
    :code:`t0 - signal_duration / 2`.
.. |ea_txt| replace:: If set to True, we consider the emitted elements also
    have an aperture. Else case, only the received elements are affected by the
    f-number (like MUST).


Same as for the setups, you can update the options anytime using:

.. code-block:: python
    :linenos:

    beamformer.update_option('name_of_option', value)


Compatibility
-------------
As specified above, all the options are not supported by all the beamformers,
or the libraries (Numpy / Numba for CPU, and cupy for GPU). This section is
listing the current support. If nothing is specified, they are all supported.

Compatibility of the :code:`interpolation` option:

.. table::
    :class: wy-table-responsive

    +---------+-------+------+--------+-------+-----------+
    | Library |       | None | Linear | Cubic | Quadratic |
    +=========+=======+======+========+=======+===========+
    | CPU     | Numpy | OK   | OK     | OK    | OK        |
    |         +-------+------+--------+-------+-----------+
    |         | Numba | OK   | OK     |       |           |
    +---------+-------+------+--------+-------+-----------+
    | GPU     | cupy  | OK   | OK     |       |           |
    +---------+-------+------+--------+-------+-----------+


Compatibility of the :code:`rx_apodization` option:

.. table::
    :class: wy-table-responsive

    +-----------------+--------+-------+
    | Library         | boxcar | tukey |
    +=========+=======+========+=======+
    | CPU     | Numpy | OK     |       |
    |         +-------+--------+-------+
    |         | Numba | OK     | OK    |
    +---------+-------+--------+-------+
    | GPU     | cupy  | OK     | OK    |
    +---------+-------+--------+-------+


Compatibility of the :code:`compound` option:

.. table::
    :class: wy-table-responsive

    +------------+-----------+-------------------------+
    | Beamformer | Reduction | Comments                |
    +============+===========+=========================+
    | DAS        | Sum       | OK                      |
    |            +-----------+-------------------------+
    |            | Mean      | |das_compound_mean_txt| |
    +------------+-----------+-------------------------+
    | FDMAS      | Both      | |fdmas_compound_txt|    |
    +------------+-----------+-------------------------+
    | p-DAS      | Both      | |pdas_compound_txt|     |
    +------------+-----------+-------------------------+

.. |das_compound_mean_txt| replace:: The 'no compound' option is supported for
    Delay And Mean, but note that all the transmissions will be preserved. This
    means that if, for a given pixel, one of the transmission is not solicited
    (due to the aperture of the element, or the transmission angle or
    whatever), its dedicated transmission will be set to 0, but there won't be
    any information about if it has been solicited or not. Therefore, if you
    want to perform the mean of these transmissions by yourself, the result
    might be different from the one with the 'compound' option.
.. |fdmas_compound_txt| replace:: The FDMAS algorithm performs the
    non-linear root / square operations on the reduced raw-focused data (summed
    or averaged). This means that the sum of the beamformed transmissions is
    not equal to the compounded beamforming.
.. |pdas_compound_txt| replace:: Same as the FDMAS algorithm, the non-linear
    operations of p-DAS are also performed on reduced data.


Compatibility of the :code:`reduce` option:

.. table::
    :class: wy-table-responsive

    +------------+-----------+-----------------------+
    | Beamformer | Reduction | Comments              |
    +============+===========+=======================+
    | DAS        | Sum       | OK                    |
    |            +-----------+-----------------------+
    |            | Mean      | |das_reduce_mean_txt| |
    +------------+-----------+-----------------------+
    | FDMAS      | Both      | |fdmas_reduce_txt|    |
    +------------+-----------+-----------------------+
    | p-DAS      | Both      | |pdas_reduce_txt|     |
    +------------+-----------+-----------------------+

.. |das_reduce_mean_txt| replace:: The 'no reduction' option is supported for
    Delay And Mean, but note that all the probe elements will be preserved.
    This means that if, for a given pixel, one of the probe element is not
    solicited (due to the aperture of the element defined with the f#), its
    dedicated element will be set to 0, but there won't be any information
    about if the element has been solicited or not. Therefore, if you want to
    perform the mean of these elements by yourself, the result might be
    different from the one with the 'reduce' option.
.. |fdmas_reduce_txt| replace:: No support, as the FDMAS reduction is a core
    part of the algorithm, this would lead to the same result as the DAS
.. |pdas_reduce_txt| replace:: No support, for the same reason as FDMAS
