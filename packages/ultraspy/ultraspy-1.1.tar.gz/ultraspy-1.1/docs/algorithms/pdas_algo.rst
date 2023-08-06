p-Delay And Sum algorithm
=========================

Algorithm
---------
Proposed by [1], it is an extension of the FDMAS algorithm consisting in doing
the squared sum of the signed squared-roots vector of delays
:math:`s_{n}(x,z)`. It allows faster computation and also can extend the
algorithms to higher degrees. This degree is characterized by the value p,
which can be an integer or a float. We can first define :math:`\tilde{r}(x,z)`,
the sum of the scaled squared signed signal along the probe elements:

.. math::
    \tilde{r}\left(x,z\right)=\sum_{n=1}^{N}\text{sign}\left(s_{n}\left(x,z\right)\right)\cdot\,{\sqrt[p]{\left|s_{n}\left(x,z\right)\right|}} \tag{1}

Then we’ll have the value of the beamformed pixel using the signed p-power:

.. math::
    r_{p-DAS}\left(x,z\right)=\text{sign}\left(\tilde{r}\left(x,z\right)\right)\cdot\,\left|\tilde{r}\left(x,z\right)\right|^{p} \tag{2}

As for the FDMAS beamformer, we then need to apply a bandpass filter, centered
at :math:`f_{0}`, in order to remove potential harmonics due to non-linear
operations, the effect of the filter is shown in the figure 3a.

.. image:: ../images/pdas_spectra.png
   :width: 600
   :align: center


Extension to In-Phase Quadrature data
-------------------------------------
As for the FDMAS, we can’t operate on the sign of a complex number as it is
undefined. Here, we’ve been using the same method as for FDMAS, also defined in
[2] and called BB-DMAS-p. It is using the same concept: separating the
amplitude and the phase in order to keep the phase unchanged while doing the
squared p-th root. It can be formulated as:

.. math::
    r_{BB-DMAS-p}=\left(\sum_{n=1}^{N}{\sqrt[p]{a_{n}\left(x,z\right)}}\cdot e^{j\phi_{n}\left(x,z\right)}\right)^{p} \tag{3}

Same as for the baseband DMAS version, when we extend it to a degree p, we see
on figure 3b that we don’t need any additional filtering. However, since we
only do the p-th root of the signal magnitude and not its phase, the
frequencies of our signal is only affected by the p-power step, which means
that the new central frequency of our beamformed signal becomes
:math:`p.f_{0}`.

TODO: Should add Ecarlat paper


- [1] A Nonlinear Beamformer Based on p-th Root Compression—Application to Plane
  Wave Ultrasound Imaging, Polichetti & al.
- [2] Ultrasound Baseband Delay-Multiply-and-Sum (BB-DMAS) nonlinear Beamforming,
  Shen & al.
