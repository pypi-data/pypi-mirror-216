.. _das_algo:

Delay And Sum algorithm
=======================

Algorithm
---------
The Delay And Sum [1] beamforming algorithm is widely used in ultrasound
imaging, as it is fast, simple, and stable. It is also greatly parallelizable,
as every pixel of the scan is independent during the computation.

For each physical location X = (x, z) within the medium we want to observe, we
need to:

- For each element of the probe, use the basic wave propagation concepts to
  find the time it took for the wave to go from the probe to the current
  location (X), and then back to the closest element in the probe, as pictured
  in figure 1
- Then, we get the closest data corresponding to these delays and we sum them.
  The resulting value is the beamforming value for X

.. image:: ../images/das_algo.png
   :width: 300
   :align: center

We are working with plane waves, so the original data is a set of M data of the
regular shape (number of probe elements ; number of time samples), with M the
number of plane waves used in one frame. Also, we want our algorithm to work
with both raw RadioFrequencies data (RFs) and In-phase Quadrature signals
(I/Qs), respectively defined as RFs and I/Qs in the following formulas. The
indices of the delays are computed and defined as :math:`\tau_{n,m}`, they
depend on the probe element n, and can be computed using regular trigonometry,
as in [1] (with :math:`\theta_m` the angle of the plane wave):

.. math::
    \tau_{n,m}\left(x,z\right)=\frac{x\cdot \cos\left(\theta_{m}\right)+z\cdot \sin\left(\theta_{m}\right)}{c}+\frac{{\sqrt[]{\left(x_{n}-x\right)^{2}+z^{2}}}}{c}  \tag{1}

Then, we can define the delayed vector is as:

.. math::
    q_{n,m}\left(x,z\right)=\text{RFs}_{m}\left(\tau_{n,\,m}\left(x,z\right)\right) \tag{2}

With n, the index of one of the N probe element, and m the index of one of the
M plane waves. Once we have the delayed vector, we just have to sum them along
the plane waves and the probe elements. The value along the probe elements is
defined by:

.. math::
    s_{n}\left(x,z\right)=\sum_{m=1}^{M}q_{n,m}\left(x,z\right) \tag{3}

Then we have the value of the beamformed data defined by:

.. math::
    r_{DAS}\left(x,z\right)=\sum_{n=1}^{N}s_{n}\left(x,z\right) \tag{4}


Extension to In-Phase Quadrature data
-------------------------------------
If we are working with I/Qs, the signal we have is the complex demodulation of
the RF data (obtained by I/Q demodulation, or Base-band demodulation, more in
section III - A). Thus, this signal is complex, respectively with the in-phase
and quadrature components as the real and imaginary parts. The beamforming
algorithm is the same here (get the delayed vectors in the I/Qs and sum them),
however, since we apply delays to our signals, we need to rotate in phase our
signals, such as [2]. We can do it using the time delays themselves (previously
defined as :math:`\tau_{n}(x,z)`), which gives the formula:

.. math::
    q_{n,m}\left(x,z\right)=\text{IQs}_{m}\left(\tau_{n,m}\left(x,z\right)\right)e^{2\cdot i\cdot\pi \cdot f_{0}\cdot\tau_{n}\left(x,z\right)} \tag{5}

Given :math:`f_0` the central frequency of the probe, which has been used for
downmixing (during the I/Q demodulation). Once we’ve computed
:math:`q_{n,m}(x,z)`, the algorithm is the same (equations 3 and 4).


- [1] So you think you can DAS? A viewpoint on delay-and-sum beamforming,
  Perrot & al.
- [2] True time-delay bandpass beamforming, Horvat & al.
