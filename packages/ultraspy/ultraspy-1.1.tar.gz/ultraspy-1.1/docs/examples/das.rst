.. _das_example:

Delay And Sum
=============

Read data
---------
In this example, we are going to go through a Delay And Sum (DAS) routine using
`ultraspy` on raw RFs simulated data from the PICMUS challenge. Those
Radio-Frequencies were simulated using FieldII on a few scatterers in an empty
homogeneous medium. We provide a Reader object to read saved data.

.. code-block:: python
    :linenos:

    from ultraspy.io.reader import Reader

    reader = Reader('/path/to/picmus_simu_rfs.hdf5', 'picmus')

If successfully loaded, an overview of the data should have been printed:

::

    ====== Loaded: ======
    Data looking like:
        data_shape: (1, 75, 128, 1527)
        data_type: float32
        is_iq: False
    Acquired with the settings:
        sampling_freq: 20832000.0
        t0: 0.0
        prf: 100.0
        signal_duration: 5e-07
        delays: (75, 128) (numpy.ndarray - float64) -> [...]
        sound_speed: 1540.0
        sequence_elements
          emitted: (75, 128) (numpy.ndarray - int32) -> [...]
          received: (75, 128) (numpy.ndarray - int32) -> [...]
    Using the probe:
    ====== Probe: ======
    name: L11-4v, with a central freq of 5208000.0Hz
    Geometry type: linear
    Probe elements:
        lateral (x): [-0.019049999999999997 ; 0.019049999999999997]
        elevational (y): [0.0 ; 0.0]
        axial (z): [0.0 ; 0.0]

Here, we've used the `'picmus'` option in the reader, meaning that it would
work only with data from the PICMUS challenge, but the extracted information
are in a specific format. Four components have been loaded:

- `data`: The data that has been loaded, a numpy array of shape (nb_frames,
  nb_transmissions, nb_probe_elements, nb_time_samples). Meaning that if we've
  recorded 25 acquisitions of a 11 plane-waves transmission using a 128 linear
  probe, the format will be `(25, 11, 128, nb_time_samples)`.

- `data_info`: A dictionary with three information: the shape of the data, its
  data type and a boolean telling if the loaded data are I/Qs or RFs.

- `acquisition_info`: A dictionary with the main information regarding the
  acquisition, including the sampling frequency, delays, PRF, etc. Those are
  detailed more in depth in the other tutorial about how to use your own data.

- `probe`: This is a probe object with the information of the used probe
  (geometry of the elements, central frequency, etc). Check out the probe class
  description in the :ref:`dedicated section<probe_class>` to pick yours.

If you want to use your own data, you will need to respect this format, or to
create your own reader option in the dedicated class. A :ref:`detailed tutorial
<simu_data_example>` on how to do this is available.


Initialize the beamformer
-------------------------

Now we're going to introduce the DAS beamformer and set the parameters /
options for our specific application:

.. code-block:: python
    :linenos:

    from ultraspy.beamformers.das import DelayAndSum

    # DAS Beamformer
    beamformer = DelayAndSum()

    # Set the information about the acquisition (probe, angles, ...) and the
    # options to use (here the transmit method, which needs to be centered for
    # PICMUS data).
    beamformer.automatic_setup(reader.acquisition_info, reader.probe)


Note that by default, `ultraspy` will try to initialize everything to work on
GPU unless you define it otherwise. You can manually initialize the CPU mode by
using :code:`beamformer = DelayAndSum(on_gpu=False)` or, if the beamformer is
already initialized, by updating its mode with
:code:`beamformer.set_on_gpu(False)`. However, if there is no GPU available on
your system (or if :code:`cupy` hasn't been installed), it'll automatically
switch back to the CPU mode. If you want to now the current mode of the
beamformer, and also its setup, you can print it (:code:`print(beamformer)`):

.. tabs::

    .. group-tab:: GPU version

        ::

            ====== Beamformer: ======
            name: das
            (on RFs, with GPU)
                emitted_probe: (3, 75, 128) (cupy.ndarray - float32) -> [...]
                received_probe: (3, 75, 128) (cupy.ndarray - float32) -> [...]
                emitted_thetas: (75, 128) (cupy.ndarray - float32) -> [...]
                received_thetas: (75, 128) (cupy.ndarray - float32) -> [...]
                delays: (75, 128) (cupy.ndarray - float32) -> [...]
                sound_speed: 1540.0
                f_number: 1.0
                t0: 0.0
                signal_duration: 5e-07
                fixed_t0: -2.5e-07
                sampling_freq: 20832000.0
                central_freq: 5208000.0
                bandwidth: 67.0
                prf: 100.0


    .. group-tab:: CPU version

        ::

            ====== Beamformer: ======
            name: das
            (on RFs, with CPU)
                emitted_probe: (3, 75, 128) (numpy.ndarray - float32) -> [...]
                received_probe: (3, 75, 128) (numpy.ndarray - float32) -> [...]
                emitted_thetas: (75, 128) (numpy.ndarray - float32) -> [...]
                received_thetas: (75, 128) (numpy.ndarray - float32) -> [...]
                delays: (75, 128) (numpy.ndarray - float32) -> [...]
                sound_speed: 1540.0
                f_number: 1.0
                t0: 0.0
                signal_duration: 5e-07
                fixed_t0: -2.5e-07
                sampling_freq: 20832000.0
                central_freq: 5208000.0
                bandwidth: 67.0
                prf: 100.0


The first line specifies if the code is running on CPU or GPU, and if it is
expecting RFs data or I/Qs (more on this in the :ref:`doppler tutorial
<doppler_example>`). The next lines are listing all the setups for the
beamforming, that you can update any time by using:

.. code-block:: python
    :linenos:

    # Additional parameters
    beamformer.update_setup('f_number', 1.75)


A list of the detailed setup and options can be found in the :ref:`beamformer
section<beamformer_class>`.


Define a Scan (region of interest)
----------------------------------

We also have to define the area of interest in our medium. Here, the probe is
~4cm wide, centered at 0, and scatterers are spread between 1 and 4.5cm depth,
so we are choosing an area covering it all:

.. code-block:: python
    :linenos:

    import numpy as np
    from ultraspy.scan import GridScan

    # Zone of interest (in m)
    x = np.linspace(-20, 20, 500) * 1e-3
    z = np.linspace(5, 50, 1000) * 1e-3

    # Or, if you want to define the grid using the lateral / axial steps you
    # want based on f0 to respect the Shannon-Nyquist theorem
    #wavelength = beamformer.sound_speed / reader.probe.central_freq
    #x = np.arange(-20e-3, 20e-3, wavelength / 4)
    #z = np.arange(5e-3, 50e-3, wavelength / 4)

    # Then define a regular grid for the beamforming
    scan = GridScan(x, z)


Beamforming
-----------

Time to perform the actual beamforming! Let's do it on the first frame of
PICMUS (there is only one anyway):

.. tabs::

    .. group-tab:: GPU version

        .. code-block:: python
            :linenos:

            import ultraspy as us

            # Get the first frame
            first_frame = reader.data[0]

            # On GPU mode, the data needs to be sent to the memory of the GPU.
            # If is also possible to send directly the numpy array, then the
            # beamformer will handle it. However, if you want to apply many
            # beamformers / setups or whatever on the same data, this will
            # prevent it to be stored multiple times on GPU
            import cupy as cp
            d_data = cp.asarray(first_frame, np.float32)

            # Actual beamforming operation, then we compute its envelope
            d_output = beamformer.beamform(d_data, scan)
            d_envelope = beamformer.compute_envelope(d_output, scan)

        The :code:`d_` prefix stands for `device`, it is a good practice to
        define your variables this way in order to keep track of what is on GPU
        or in CPU. Also note that the beamformed signals are still on GPU for
        now, so we now can use them for something else if needed (Doppler
        imaging for example).

        Now that we have the envelope, we just want to convert it to B-Mode,
        then recover the data from the GPU memory to the CPU, in order to
        display it using :code:`matplotlib`.

        .. code-block:: python
            :linenos:

            # Get the B-Mode to display
            us.to_b_mode(d_envelope)

            # Get the B-Mode back on CPU memory
            b_mode = d_envelope.get()


    .. group-tab:: CPU version

        .. code-block:: python
            :linenos:

            import ultraspy as us

            # Get the first frame
            first_frame = reader.data[0]

            # Actual beamforming operation, then we compute its envelope
            output = beamformer.beamform(first_frame, scan)
            envelope = beamformer.compute_envelope(output, scan)

            # Get the B-Mode to display, using ultraspy.cpu lib
            b_mode = us.cpu.to_b_mode(envelope)


All good, time to display the B-Mode:

.. code-block:: python
    :linenos:

    import matplotlib.pyplot as plt
    extent = [x * 1e3 for x in [x[0], x[-1], z[-1], z[0]]]  # In mm
    plt.imshow(b_mode.T, extent=extent, cmap='gray', clim=[-60, 0])
    plt.title('DAS on PICMUS - 75 plane waves')
    plt.xlabel('Axial (mm)')
    plt.ylabel('Depth (mm)')
    plt.show()


.. image:: ../images/das_bmode.png
   :width: 600

And voilà! Feel free to have a look to the next tutorial (about Doppler) if you
want to see another application of `ultraspy`.
