.. _architecture:

Architecture
============
This section aims to describe the architecture choices of the `ultraspy` lib,
which is composed of the following classes:

.. image:: ../images/ultraspy_classes.png
   :width: 800


and organized as followed:

::

    ultraspy/
    ├── beamformers/
    |   ├─── beamformer.py
    |   ├─── setups.py
    |   ├─── options.py
    ├── probes/
    |   ├─── configs/
    |   ├─── probe.py
    ├── gpu/
    ├── cpu/
    ├── file_loaders/
    ├── helpers/
    ├── utils/
    ├── reader.py
    ├── metrics.py

The notable directories are:

* :code:`beamformers/`: Directory with all the implemented beamformers, it
  contains the parent class Beamformer, and some implementations (das.py,
  fdmas.py, ..), and also the setups and the options of the beamformer. More on
  this in the :ref:`beamformer class section <beamformer_class>`.

* :code:`probes/`: Directory with the Probe classes and all the supported
  probes.

* :code:`gpu/`: Directory with the common methods of ultraspy implemented in
  GPU (check out the :ref:`dedicated section <common_methods>`.).

* :code:`cpu/`: Same as :code:`gpu/` directory but with the CPU methods.

* :code:`reader.py`: The reader file, that converts the data file into
  something understandable by the Beamformer class. More in the :ref:`dedicated
  section <reader_class>`.).

* :code:`metrics.py`: The metrics file, with all the evaluation methods (SNR,
  CNR, PSL, ...). More in the :ref:`dedicated section<common_methods>`.).

* :code:`file_loaders/`: Directory with the loaders for the data file, given
  their extension.

* :code:`helpers/`: Directory with the helpers for our methods.

* :code:`utils/`: Some utility files.


.. toctree::
   :maxdepth: 1

   beamformer_class
   probe_class
   scan_class
   reader_class
   common_methods
