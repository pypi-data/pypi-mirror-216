.. _doppler_example:

Doppler
=======
Detailed example of a color and power doppler on raw RF real data, scanning a
rotating disk. Few steps will be seen very quickly, as we assume you've already
checked out the :ref:`DAS example <das_example>`.


Beamforming process
-------------------

We first read the data (`'must'` reader), initialize the scan we'd like to
observe, and initialize a basic DAS beamformer.

.. code-block:: python
    :linenos:

    import numpy as np
    import cupy as cp
    from ultraspy.io.reader import Reader
    from ultraspy.scan import GridScan
    from ultraspy.beamformers.das import DelayAndSum
    import ultraspy as us

    # Load the data
    reader = Reader('/path/to/rotating_disk.mat', 'must')

    # Medium to observe
    x = np.linspace(-12.5, 12.5, 250) * 1e-3
    z = np.linspace(10, 35, 250) * 1e-3
    scan = GridScan(x, z)

    # DAS Beamformer, with the I/Q option set to True, as we need to work on
    # phase-shifts for Doppler
    beamformer = DelayAndSum(is_iq=True)
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)

So far, nothing new but the :code:`is_iq` option. The loaded data is RFs, but
in order to perform Doppler operations, we'll have to convert them into I/Qs,
thus we need to warn the beamformer to set itself in the I/Qs algorithms mode.

.. tabs::

    .. group-tab:: GPU version

        .. code-block:: python
           :linenos:

            # Send the whole packet to GPU, as complex data so we can store I/Qs
            d_data = cp.asarray(reader.data, np.complex64)

            # Conversion, required some info about the acquisition
            info = beamformer.setup
            us.rf2iq(d_data, info['central_freq'], info['sampling_freq'],
                     beamformer.t0)


    .. group-tab:: CPU version

        .. code-block:: python
           :linenos:

            # Conversion to I/Qs, required some info about the acquisition
            info = beamformer.setup
            data = us.cpu.rf2iq(data, info['central_freq'],
                                info['sampling_freq'], beamformer.t0)


Then we need to beamform the whole packet at once:

.. tabs::

    .. group-tab:: GPU version

        .. code-block:: python
           :linenos:

            d_beamformed_packet = beamformer.beamform_packet(d_data, scan)


    .. group-tab:: CPU version

        .. code-block:: python
           :linenos:

            beamformed_packet = beamformer.beamform_packet(data, scan)


.. warning::
    Note that the :code:`beamform_packet` might require a big volume of memory,
    if the packet is too large, consider to split it in bunches of iterates
    through frames.


Doppler Imaging
---------------

And voilà! We have everything we need! Time to actually compute the doppler
maps now. For the Color Doppler, the nyquist velocity needs to be computed
beforehand. The Power Doppler on the other hand can be computed solely with the
beamformed I/Qs.

.. tabs::

    .. group-tab:: GPU version

        .. code-block:: python
           :linenos:

            # We need to know the nyquist velocity for the color-map
            nyquist = info['sound_speed'] * info['prf'] / (4 * info['central_freq'])

            # Doppler maps
            d_color_map = us.get_color_doppler_map(d_beamformed_packet, nyquist)
            d_power_map = us.get_power_doppler_map(d_beamformed_packet)
            color_map = d_color_map.get()
            power_map = d_power_map.get()


    .. group-tab:: CPU version

        .. code-block:: python
           :linenos:

            # We need to know the nyquist velocity for the color-map
            nyquist = info['sound_speed'] * info['prf'] / (4 * info['central_freq'])

            # Doppler maps
            color_map = us.cpu.get_color_doppler_map(beamformed_packet, nyquist)
            power_map = us.cpu.get_power_doppler_map(beamformed_packet)


This is enough for the Doppler imaging, let's compute the B-Mode of one of the
frame (let's say the last one) for better visualization.

.. tabs::

    .. group-tab:: GPU version

        .. code-block:: python
           :linenos:

            d_last_beamformed = d_beamformed_packet[..., -1].copy()
            d_envelope = beamformer.compute_envelope(d_last_beamformed, scan)
            us.to_b_mode(d_envelope)
            b_mode = d_envelope.get()


    .. group-tab:: CPU version

        .. code-block:: python
           :linenos:

            last_beamformed = beamformed_packet[..., -1].copy()
            envelope = beamformer.compute_envelope(last_beamformed, scan)
            b_mode = us.to_b_mode(envelope)


And we're done! We can now display the final result. For the color-map, it is
common to use the power estimations as a threshold for nicer visualizations.
Here, we'll set it to -20dB.

.. code-block:: python
    :linenos:

    import matplotlib.pyplot as plt

    # Power threshold for color map
    power_threshold = -20
    doppler_colormap = us.get_doppler_colormap()

    # Display init
    extent = [x * 1e3 for x in [x[0], x[-1], z[-1], z[0]]]  # In mm
    fig, axes = plt.subplots(1, 2)

    # Color map, we show the B-Mode first, then the masked color-map
    color_map = np.ma.masked_where(power_map < power_threshold, color_map)
    axes[0].imshow(b_mode.T, extent=extent, cmap='gray', clim=[-60, 0])
    im1 = axes[0].imshow(color_map.T, extent=extent, cmap=doppler_colormap,
                         clim=[-nyquist, nyquist])
    fig.colorbar(im1, ax=axes[0])
    axes[0].set_title('Color map (doppler velocity (m/s))')

    # Power map
    im2 = axes[1].imshow(power_map.T, extent=extent, cmap='hot', clim=[-30, 0])
    axes[1].set_title('Power map (dB)')
    fig.colorbar(im2, ax=axes[1])

    plt.show()


.. image:: ../images/doppler.png
   :width: 800

There we go :) Feel free to have a look to the next tutorial (about metrics) if
you want to see another application of ultraspy.
