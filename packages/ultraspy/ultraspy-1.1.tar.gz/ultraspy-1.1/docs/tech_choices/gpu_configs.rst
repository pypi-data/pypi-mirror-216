GPU using Python
================

The problem we are facing
-------------------------
Even if DAS is really straightforward and fast, it is not the case of all of
the beamforming algorithms, and some of them can really benefit from a GPU
implementation if it is correctly done. In order to do that, we need to first
define and understand how the GPU works.

On the CPU, we have one very powerful processing unit that can perform complex
operations one at a time, meanwhile on the GPU, we have a lot of very basic
processing units. The CPU processing capability is much more efficient than any
of the GPU’s, however, it can only run one operation at a time, while the GPU
can parallelize many operations, but is very slow if the computation is too
complex. To sum up, on CPU, we need to vectorize as much as possible our
algorithms, so the CPU has one big job at a time (matrix manipulations),
however on GPU, it is the opposite; we need to divide all jobs as much as
possible, so every thread run very simple dedicated operation.

On beamforming algorithms, every pixel is computed separately: they are all
independent. The GPU seems to be very adapted as it would be able to
parallelize the computation of many pixels at a time, but we need to adapt our
implementation so nothing is vectorized from one pixel to another.


What we can do using the GPU
----------------------------
When implementing the beamforming algorithms on the GPU, we are writing
kernels, which will be pieces of code in C++ and which will be run on every
pixel at the same time. These kernels have a few limitations in order to be
Cuda-compatible:

- As the code is pre-computed and won’t run on the fly, the device needs to
  know beforehand how much memory it will need. We can’t allocate variables of
  dynamic size within our code
- Since we can’t dynamically allocate memories, almost no external libraries
  can be used, so all our algorithms need to be implemented completely. As
  we’ll see, it will be a problem in some of our algorithms (need to implement
  matrix inversion, filtering… which requires a good knowledge of linear
  algebra)

Once we’ve defined these restrictions, we need to define how to organize the
parallelization and how to organize our memory allocations.

Grids and blocks
^^^^^^^^^^^^^^^^
On the GPU, we have a lot of threads, but we can’t just run them all: we need
to organize them so we make sure most of the threads are working most of the
time. By convention, we divide them in a grid of blocks of threads. As shown in
figure below, if we choose blocks too big, some of them won’t be filled (right
border of the grid). That said, if we have T maximum number of threads
(physically defined by the GPU specifications), and we want to run P operations
(P > T), the most intuitive definition of our grid and block dimensions is
:math:`\text{block}_{\text{dim}}=(T,1,1)` and
:math:`\text{grid}_{\text{dim}}=(dx + (mx+1),1,1)`, given
:math:`dx,mx=\text{divmod}(\frac{P}{T})`. It might not be optimal and can be
adapted depending on our application.

Note that GPUs are organized in 3D, which can be useful if neighboring pixels
affect each other in a 3D world (GPUs are often used in video games). In our
case, we will have 3D environments, but pixels are independent, so we can play
1D for simplicity.

.. image:: ../images/block_grid.png
   :width: 300
   :align: center

Shared memory
^^^^^^^^^^^^^
.. image:: ../images/gpu_architecture.png
   :width: 600
   :align: center

When calling the kernels from the host (CPU), we can allocate some data within
the device. This data is going to the global memory, which can be accessible to
all our threads at any time, but “quite” slowly. Within the kernel, we can
allocate some small variables of defined size, and these are defined in the
registers which are very fast. If needed, there is also another kind of memory,
called the shared memory, which is shared to all the threads within a block. It
is bigger than registers, and faster than global memory. Considering this, we
could imagine some applications where we adapt the size of our blocks so they
can share some big amounts of memory.

It is important to know that because most of the memory allocations are done by
the device, and we can have slow processes if we don’t know where the data
went.


Libraries
---------
We’ve tried a few libraries on both CPU and GPU to compare their efficiencies:

- Numpy: This is one of the most common libraries for matrix manipulation on
  CPU. It has a lot of methods already implemented (filtering, matrix
  inversion, fourier transformation, ...), is widely documented and easy to
  use. It is especially efficient when we manage to vectorize our algorithms.
  This can be used by setting the environment variable 'ULTRASPY_CPU_LIB' to
  'numpy'
- Numba: This library adapted many of Numpy functions into C++ code, which can
  be called from Python. C++ is known for being much faster for this kind of
  computation, but also can’t deal with the same level of abstraction. Then, if
  we are adapting our implementation to simpler code (no vectorization), it can
  be converted easily and fasten up the code. This implementation happens to be
  the same as the one for GPU. This is the default CPU lib, but can be set like
  Numpy by setting the environment variable 'ULTRASPY_CPU_LIB' to 'numba'
- Cupy: Cupy runs on GPU, with a set of high level functions similar to Numpy,
  along with a low level RawKernel, which allows to write our own Cuda kernels.
  It requires us to write all our kernels in C++ and is the lowest level of
  abstraction, however it is also the most efficient because we have full
  control of what we are doing

