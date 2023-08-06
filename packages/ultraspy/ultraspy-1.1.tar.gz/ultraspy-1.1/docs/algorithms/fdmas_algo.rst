Filtered Delay Multiply And Sum algorithm
=========================================

Algorithm
---------
Proposed in [1], the Filtered Delay Multiply And Sum (FDMAS) algorithm is quite
similar to DAS, except for the reduction step: while DAS was reducing the
vector of delays (:math:`s_{n}(x,z)`) by summing it along the probe elements,
FDMAS is multiplying all of them in pairs. This technique aims to reduce the
“moustaches” effect observed with the DAS algorithm. Indeed, with DAS, if one
of the element of :math:`s_{n}(x,z)` is salient, the resulting
:math:`r_{\text{DAS}}(x,z)` will be strong as well, even if all the other
elements of the delays vector are weak, FDMAS is minimizing this effect by
combining elements together.

Given two distinct elements of the probe n and n', we can define
:math:`s_{n,n'}(x,z)=s_{n}(x,z).s_{n'}(x,z)`. Then, the FDMAS formula is:

.. math::
    r_{FDMAS}\left(x,z\right)=\sum_{n=1}^{N-1}\sum_{n^{\prime}=n+1}^{N}\text{sign}\left(s_{n,n^{\prime}}\left(x,z\right)\right)\cdot\,{\sqrt[]{\left|s_{n,n^{\prime}}\left(x,z\right)\right|}} \tag{1}

Note that, in order to preserve the dimensionality of the signals in volt, we
have to square root the resulting multiplication. Also, we need to pay
attention to the sign of the multiplication as it disappears within the square
root.

Furthermore, when we are multiplying two similar signals (centered at
:math:`f_{0}`), we are generating two frequency bands at both
:math:`f_{0}-f_{0}` and :math:`f_{0}+f_{0}` frequencies (respectively DC and
second harmonics). So we also need to apply a BandPass filter to extract the
second harmonics only (using a band-pass filter centered at :math:`2.f_{0}`).
The figure 1 is showing an example of the effect of this bandpass filter. In
order to avoid potential aliasing with the second harmonics, we also
oversampled the original RFs data, so we can make sure the :math:`2.f_{0}`
frequency is below the Nyquist frequency.

.. image:: ../images/fdmas_spectra.png
   :width: 600
   :align: center


Extension to In-Phase Quadrature data
-------------------------------------
There is some complication here: the sign of a complex number is undefined,
and since we’re working on I/Q signals, it causes a problem. [2] proposed a
solution to adapt FDMAS for baseband signals (called BB-DMAS). In this version,
only the reduction part changes (it is computing the delays vector
:math:`s_{n}(x,z)` the same way as DAS or RFs version of FDMAS do).
Considering :math:`s_{n}(x,z)` as a vector of complex numbers, we can extract
their modulo and phase to rewrite them as
:math:`s_{n}(x,z)=a_{n}(x,z).e^{i\phi_{n}(x,z)}`, and then only scale the
magnitudes of our signals, which preserves their phases. Then the BB-DMAS is
defined as the unsigned square of the sum of the scaled data, which can be
formulated as:

.. math::
    r_{BB-DMAS}=\left(\sum_{n=1}^{N}{\sqrt[]{a_{n}\left(x,z\right)}}\cdot e^{i\,\phi_{n}\left(x,z\right)}\right)^{2} \tag{2}

This method is performing the combination of all the elements twice (both pairs
of n by m and m by n), and also pairing the diagonal (n by n) which wasn’t done
on RFs. However, as explained in [3], the diagonal term is negligible compared
to the rest of the unsigned equation, so it can be added up without altering
the results too much.

About the filtering, as shown in the figure 2b, the beamformed signal doesn’t
need any extra filtering step, as it has only generated second harmonics.



- [1] The Delay Multiply and Sum Beamforming Algorithm in Ultrasound B-Mode
  Medical Imaging, Matrone & al.
- [2] Ultrasound Baseband Delay-Multiply-and-Sum (BB-DMAS) nonlinear Beamforming,
  Shen & al.
- [3] A Nonlinear Beamformer Based on p-th Root Compression—Application to Plane
  Wave Ultrasound Imaging, Polichetti & al.

