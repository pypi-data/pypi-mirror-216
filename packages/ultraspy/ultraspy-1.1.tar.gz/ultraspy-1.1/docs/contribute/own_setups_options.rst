Add your own setups / options
=============================

Setups
------
You can add a setup within the :code:`beamformers/setups.py` file. Then you can
simply adjust it using:

.. code-block:: python
    :linenos:

    beamformer.update_setup('name_of_setup', value)

Then the setup will be accessible from the :code:`beamform` method using
:code:`self.setups['name_of_setup']`.


Options
-------
You can add a option within the :code:`beamformers/options.py` file. Then you
can simply adjust it using:

.. code-block:: python
    :linenos:

    beamformer.update_option('name_of_option', value)

If you want the option to be accessible by any beamformer, you should add it to
the dedicated kernels. Those are made to be quite flexible, let's say for the
interpolation, you are able to add your own within the interpolation kernels,
and then add it as a possible option value.
