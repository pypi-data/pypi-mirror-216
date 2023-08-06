Prepare the code
================

Install the code from source
----------------------------
You need to :ref:`install<installation>` the code from source. The installation
tutorial already details how to do that properly.


Prepare your environment for testings
-------------------------------------
The lib is a set of methods and classes to perform ultrasound imaging
operations, and it is provided with a set of unit and integration tests. The
better way to make sure the lib isn't broken and works properly is to make sure
all these tests can run without errors. This is a routine to make sure the code
is stable, and you should run it whenever you modify anything, in order to
avoid regression.

The tests are validated on some sample data, both experimental and from
simulation, that can be downloaded using the
:code:`resources/download_resources.py` script:

.. code-block:: console

    $ cd resources
    $ python download_resources.py

If you are using a GPU environment, you will also need to update the version of
:code:`cupy` you are using within the :code:`requirements_gpu.txt`. It should
be based on the CUDA version you have installed, as specified in the
:ref:`installation<installation>` section.


The tox routine
---------------
Last but not least, you should have a look to the :code:`tox.ini` file, which
is listing the routine to perform. The main section is the first one:

::

    [tox]
    envlist =
        ; CPU
        cpu_tests
        ; GPU, comment the next line if you are on a CPU only system
        gpu_tests
        ; Generate documentation
        docs
    skipsdist = true

Each line is running a distinct testing environment, one for the tests on CPU,
another one for the ones in GPU, and the last one is generating the present
documentation using Sphinx. If you don't have a GPU on your system, you should
comment the :code:`gpu_test` line.

You should also note the second section, which contains the
:code:`ULTRASPY_CPU_LIB` line, which is commented. By default, the CPU code
runs using the Numba library which is faster. If you want to test the Numpy
lib, which is using matricial operations, you can uncomment this line to set
the environment variable accordingly.

If everything is set as you want, you can run the routine using:properly.

.. code-block:: console

    $ pip install tox
    $ tox

If this succeeded, then you're all set!
