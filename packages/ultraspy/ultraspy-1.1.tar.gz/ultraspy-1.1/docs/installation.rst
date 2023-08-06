.. _installation:

Installation
============

Prepare your computer
---------------------
If you plan on using :code:`ultraspy` solely on CPU, there is nothing to do to
prepare your system, just make sure that your Python version is above 3.8.
However, if you plan on using the GPU version of the lib, CUDA and :code:`cupy`
must be installed.

.. warning::
    The Python version must also be below 3.11, as the Numba library is not yet
    compatible, as mentioned in https://github.com/numba/numba/issues/8304 . If
    you see that this issue is now solved, you can remove this warning and
    update the :code:`python_requires` line within the `setup.py` file with
    :code:`python_requires='>=3.8, <4',`

Concerning CUDA, you can find all the directives in their `dedicated download
website <https://developer.nvidia.com/cuda-downloads>`__. You'll have to
provide various information about your system (OS, version, etc) and follow the
instructions (depending on the version, you might have to add cudnn or to
configure manually your PATH and CUDA_PATH environment variable).

.. note::
    The version of CUDA must be one of the supported version by :code:`cupy`.
    Check out the list of supported CUDA versions `here
    <https://docs.cupy.dev/en/stable/install.html>`__, and make sure to pick
    one of them.

Now you're ready to install `cupy <https://cupy.dev/>`__, this can be done by
running the pip command:

.. code-block:: console

    $ # Replace the XXx by the CUDA version you picked
    $ # Examples: 10.2 -> 102, 11.7 -> 117, ...
    $ pip install cupy-cudaXXx

If you are working with a Windows environment, the last step is to make sure
that you have a C compiler ready in your computer. On Linux OS, you should be
able to skip this step. Also it hasn't been tested yet, but this should be the
same for MacOS.

However, if you are working on Windows, the easiest way to install a compiler
is to get Visual Studio C++, which provides the compilers in C and C++ for our
CUDA kernels. This one can be installed from
`there <https://visualstudio.microsoft.com/downloads/>`__. Once downloaded,
you'll have to select the Desktop development with C++ tool. The newly
installed C/C++ package need to be accessible by your system, so you will have
to add the path to the cl.exe in your PATH. Its location depends on the Visual
Studio version, but you might find it in one of the following directory:

::

    - C:\Program Files\Microsoft Visual Studio X.x\VC\bin\
    - C:\Program Files\Microsoft Visual Studio\XXXX\Community\VC\Tools\MSVC\14.32.31326\bin\Hostx64\x64\

Since the system environment variables have been changed, you also need to
restart your system so it refreshes them.


From pypi
---------
The easiest way to install ultraspy is to do it using pip from pypi.

.. code-block:: console

    $ pip install ultraspy


Check the installation
----------------------
It's time to make sure the installation worked as expected. You can import both
:code:`cupy` and :code:`ultraspy` in a Python console to check if everything is
ready:

.. code-block:: python

    import cupy
    import ultraspy

From there, as an user, you should have a look to the :ref:`examples<examples>`
section.


Installation from source
------------------------
You might need to use and compile the code from source if you want to add your
own algorithms. In order to do that, you'll first need to clone the code
from the git.

.. code-block:: console

    $ git clone https://gitlab.com/pecarlat/ultraspy.git

The first thing to do in order to make sure the cloned code works properly,
so we can be sure the system has been properly configured. To do that, we've
integrated a tox routine that go through the code, runs a set of unit tests to
ensure the methods are runnable and work properly, and then compile the
documentation you are currently reading. The detailed information concerning
this can be found in the :ref:`contribute section<contribute>`.
