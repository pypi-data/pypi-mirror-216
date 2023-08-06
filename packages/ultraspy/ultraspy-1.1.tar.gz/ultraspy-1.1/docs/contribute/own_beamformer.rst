Add your own beamformer
=======================

Your own beamformer tutorial
----------------------------
If you want to build a new beamformer, let's call it xDAS, you'll first need to
create its dedicated class in :code:`ultraspy/beamformers/xdas.py`. This class
should inherit from the :code:`Beamformer` class, and needs to override either
the :code:`beamform_gpu` or :code:`beamform_cpu` methods (or, better, both).
The 'clean' way to implement them is to use them to call the kernels of the
beamforming directly. Those can be implemented along with others in either:

- :code:`gpu/kernels/beamformers/xdas.cu` for the GPU kernel, in CUDA
- :code:`cpu/kernels/numba_cores/xdas.py` for the CPU kernel, in Numba, using
  @nopython mode
- :code:`cpu/kernels/numpy_cores/xdas.py` for the GPU kernel, in Numpy, using
  matricial operations

The minimum arguments for the :code:`beamform` methods (both CPU and GPU) are
the data and a scan, with the information of the pixels to beamform.


Notes on CUDA kernels
---------------------
When writing a CUDA kernel, you will need to define the core codes, that are
dealing with any kind of data. Let's say if you want xDAS to be flexible to
both RFs and I/Qs data, you should build two constructors, one for data of
float type (RFs), and another one to handle complex type (I/Qs):

.. code-block:: cuda
    :linenos:

    extern "C" {
        __global__ void xdas_float(const float *data, ...) {
            // Get the index of the current pixel we are beamforming
            const int i = threadIdx.x + blockDim.x * blockIdx.x;
            if (i < nb_pixels) {
                core_xdas(data, ...)
            }
        }

        __global__ void xdas_complex(const complex<float> *data, ...) {
            // Get the index of the current pixel we are beamforming
            const int i = threadIdx.x + blockDim.x * blockIdx.x;
            if (i < nb_pixels) {
                core_xdas(data, ...)
            }
        }
    }


Then, the core code of the beamformer will be in the :code:`core_xdas`, which
now can handle both data types using a C++ template:

.. code-block:: cuda
    :linenos:

    template <class T>
    __device__ void core_xdas(const T *data, ...) {
        // Core code
    }


The kernel now needs to be added within the
:code:`gpu/kernels/beamformers_kernels.py` file, in order to tell `ultraspy`
how to compile it:

.. code-block:: python
    :linenos:

    # These kernels are within the 'beamformers' directory
    DIR = 'beamformers'

    # Compile the code as a binary .cubin file
    mod_xdas = compile_bin(DIR, 'xdas.cu')

    # Get all the local kernels, given the type of the first argument
    _k_xdas_types = {
        GPUTypes.FLOAT.value: mod_xdas.get_function('xdas_float'),
        GPUTypes.COMPLEX.value: mod_xdas.get_function('xdas_complex'),
    }

    # k_xdas will automatically redirects to the proper kernel given the type
    # of the data
    k_xdas = call_function_given_type(_k_xdas_types)


You can now import and call the kernel from the :code:`beamform_gpu` method of
your beamformer:

.. code-block:: python
    :linenos:

    from ultraspy.gpu import gpu_utils
    from ultraspy.gpu.kernels.beamformers_kernels import k_xdas

    class xDAS(Beamformer):
        ...

        def beamform_gpu(self, d_data, scan):
            g_dim, b_dim = gpu_utils.compute_flat_grid_size(nb_pixels)
            k_xdas(g_dim, b_dim, (d_data, ...))


About the kernel itself, it will mainly depend on the operation you want to
perform, but note that, at compilation, we consider that the working directory
of our compiler is the .cu file's emplacement, Which means that you can include
any other .cu files already implemented, especially the interpolation /
transmission / apodization... DAS provides a good example of use.
