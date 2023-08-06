Beamformers optimization on GPU
===============================

DAS
---
No real limitations here, if we don’t vectorize the algorithm, it just has to
be a double for-loop (along the plane waves and then the probe elements). Every
pixel is independent, so we don’t see the point of using shared memory here.
The grid / blocks can be organized in the most basic way.

However, we’ve noted that the time delays for a given position X (defined as
:math:`\tau_{n,m}(x,z)` in our equations) only depends on the dimension of the
medium we are scanning, and not on the data. It means that it can be computed
only once, and might fasten up the computation time if we extract it from our
kernel. Turned out that the time delays are actually really trivial to compute
and, since we need to loop over all the elements of the scan anyway, it ain't
much faster. Furthermore, it is also really heavy in memory as we need to keep
a matrix of size :math:`n_{x}\times n{z}\times N\times M`.


FDMAS
-----
This algorithm is a typical example of how beneficial the GPU can be for our
applications. Indeed, the multiplication of all the elements of
:math:`s_{n}(x,z)` by pairs can’t be vectorized as all the pixels of the scan
have a vector of different sizes (depending on the f#). It means that we need
to preserve a for-loop, which is really inefficient on CPU.

About the reduction step itself (the multiplication), we’ve tried two
approaches, a straightforward one, where we use one thread per pixel, each of
them doing the whole computation process, and another one where we are using
the shared memory, as described in figure below. The idea behind this second
method is to have one block per pixel, which will be composed of a few threads,
each of them dedicated to one of the pair multiplication. Thus, the
parallelization is reinforced.

If the idea of the second method was programmatically interesting (and might be
useful later), it appears that the multiplication process was way too trivial
to gain from being parallelized and we are actually losing time when
synchronizing the threads after the multiplication steps.

.. image:: ../images/fdmas_optim_gpu.png
   :width: 600
   :align: center


p-DAS
-----
There is nothing specific here, the implementation can’t be more parallelizable
than DAS, and we can do the implementation the same way, just changing the
reduction step.
