.. _simu_data_example:

Simulate and use your own data
==============================
Here, we are going to simulate some data using the `SIMUS simulator
<https://www.biomecardio.com/MUST/functions/html/simus_doc.html>`_. As for this
tutorial, let's simulate a convex probe emitting ultrasound in a very simple
medium with a single scatterer. The SIMUS simulator has its own detailed
documentation, so we won't go too much in detail here.

First, let's build a medium, load a probe and define the emission sequence
(five plane waves) :

.. code-block:: matlab
    :linenos:

    % Single scatterer medium, centered
    x = [0]; y = [0]; z = [25e-3];
    amp = ones(1, 1);

    % Simple convex probe (the C5-2v)
    param = getparam('C5-2v');

    % Compute the delays of the plane wave
    param.fs = 4*param.fc;
    angles = [-10, -5, 0, 5, 10];
    nb_a = size(angles, 2);
    delays = txdelay(param, deg2rad(angles));

To build the simulation, we need to create a container and to launch the
simulation for each sequence :

.. code-block:: matlab
    :linenos:

    RF = cell(nb_a, 1);
    Nts = zeros(1, nb_a);
    for k = 1:nb_a
        RF{k} = simus(x, y, z, amp, delays(k, :), param);
        Nts(k) = size(RF{k}, 1);
    end

Since all the sequences will have a different number of time sample and
different t0, we want to re-organize this in order to have a uniform number of
time samples :

.. code-block:: matlab
    :linenos:

    nt = max(Nts);
    for angle = 1:nb_a
        [nnt, nne] = size(RF{angle});
        RF{angle} = cat(1, RF{angle}, zeros(nt - nnt, nne));
    end
    RF = cat(3, RF{:});

There we go! Now we have the data, of shape (nb_time_samples, nb_probe_element,
nb_sequences), which is all we need, you can save them in a .mat file.

Let's now see how ultraspy reads the data files. So far, three data file
extensions are implemented : .mat, .hdf5, and .rff256 (UlaOp format). You can
add your own in the _file_loaders/ directory as a python class, child of the
FileLoader class. Those should read the data file and store all the data as a
dictionary within :code:`self.data`. The three examples should be enough if you
want to add your own extension so there is no need to detail much the process
here, but just don't forget to add the new extension within the
`_file_loaders/factory.py` file.

Now that we can read any data format and store everything within a python
dictionary, we should define how to interpret them. From now on, the magic
happens in the `reader.py` file. The first thing is to define a identifier for
your data format, let's call ours :code:'tuto_simu'. You should add it to the
list of the :code:`available systems`, within the :code:`__extract_data`
method, and then you can create your own :code:`__extract_tuto_simu_data`.

Within :code:`__extract_tuto_simu_data(loaded_dict)` we will have access to all
the data within :code:`loaded_dict`. The first thing is to give the information
about the probe that we've used. There's a few ways to build the probe.

.. code-block:: python
    :linenos:

    from ultraspy.probes.factory import build_probe

    # If we have the name of the probe and if the probe has been defined within
    # the probe class
    probe = get_probe('C5-2V')

    # If we don't, but have all the needed information
    probe = build_probe(geometry_type='convex',
                        nb_elements=128,
                        pitch=0.508e-3,
                        central_freq=3.57e6,
                        bandwidth=79,
                        radius=49.57e-3)

A good practice is to include the name of the probe within the data file, and
then to add all the information as a Probe class so you are sure that you are
always using the one from the config you've defined. You can also verify the
geometry using :

.. code-block:: python
    :linenos:

    probe = probe.show()

.. image:: ../images/convex_probe.png
   :width: 600

Nice, now we need to load the data, which is expected to be of the shape
(nb_frames, nb_transmissions, nb_probe_elements, nb_time_samples). So we need
to reorganize the data to make it match. You also need to store the information
about this data within a dedicated dictionary.

.. code-block:: python
    :linenos:

    # Change the shape of the data
    data = loaded_dict['RF'].transpose(2, 1, 0)[None, :]
    data_info = {
        'data_shape': data.shape,
        'data_type': data.dtype,
        'is_iq': False,
    }

Next, something important is to provide the delays of the signals. Here, we've
generated 5 sequences of 128 elements. Each sequence have distinct delays per
element in order to emit tilted plane waves. Those were made to match five
tilting of [-10, -5, 0, 5, 10] degrees. Let's generate them :

.. code-block:: python
    :linenos:

    from ultraspy.transmit_delays_helpers import compute_pw_delays

    # Get the tilting angles
    angles = [-10, -5, 0, 5, 10]

    # Compute the delays
    delays = compute_pw_delays(np.radians(angles), probe,
                               speed_of_sound=1540,
                               transmission_mode='positives')

    # Visualize the results
    probe.show_delays(delays)

.. image:: ../images/convex_delays.png
   :width: 600

Now we have our delays, of shape (nb_cycles, nb_elements). We've generated them
by ourselves, but the good way would have been to store them in the data file,
since each echograph has its own way to deal with delays.

Finally, we also need to define which sequence has been emitted, meaning that,
for each cycle, which elements have been triggered, both for emission and
reception. Here, in a plane wave scenario, they've all been used for both
emission and reception, so we can define :

.. code-block:: python
    :linenos:

    import numpy as np

    nb_transmissions = delays.shape[0]
    elements_indices = np.arange(probe.nb_elements)
    sequence = {
        'emitted': np.tile(elements_indices, (nb_transmissions, 1)),
        'received': np.tile(elements_indices, (nb_transmissions, 1)),
    }

Nice we are all set! The last thing to do is to store all these data within the
four class attributes :

.. code-block:: python
    :linenos:

    self.data = data
    self.data_info = data_info
    self.acquisition_info = {
        'sampling_freq': 4 * probe.central_freq,
        't0': 0,
        'prf': None,
        'signal_duration': None,
        'delays': delays,
        'sound_speed': 1540,
        'sequence_elements': sequence,
    }
    self.probe = probe

All good! Now we have all we need, the reader can now be safely used using :

.. code-block:: python
    :linenos:

    reader = Reader(my_data_file, 'tuto_simu')

The same procedure can be followed for data from Field II ; an example on how
to generate 3D simulation is by the way available within
`resources/external_codes` and the dedicated reader also exists (simu_3d). A
version exists already for the Verasonics and the UlaOp data, but those are not
maintained, and might only work on very specific situations.
