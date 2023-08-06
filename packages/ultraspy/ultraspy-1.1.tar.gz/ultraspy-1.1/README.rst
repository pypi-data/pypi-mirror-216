What is ultraspy?
-----------------
Ultraspy is a package designed to efficiently manipulate ultrasound data using
GPU. The most common beamforming or Doppler methods are implemented (such as
DAS, RF to I/Qs, Color/Power Doppler, ...), along with some state-of-the-art
methods (Capon beamforming, Vector Doppler, alias-free Doppler velocity, ...).
A set of metrics (PSL, FWHM, SNR) is also provided so anyone can validate the
quality of their ultrasound data and beamforming operations.

The package is designed to work with both RF and I/Q signals, in 2D or 3D, and
with any type of probe (linear, convex, or matrix). The core code can run both
on CPU and GPU, making it ideal for any real-time application. All beamforming
parameters (f-number, compounding, apodization…) can be freely customized at
any time for research purposes.

The package has been thought to be as flexible as possible, so that anyone
could eventually clone it and add its own research methods and test it in real
time. A set of tutorials is provided to facilitate user learning and adoption,
along with some instruction on how to contribute to the lib if you feel like
your research method should be added to help the community.


Features
========
- General beamforming methods, flexible to Radio-Frequency or In-phase
  Quadrature data, working on CPU and GPU. Mainly DAS and FDMAS for the
  plane-wave imaging, but also TFM for Beam Focusing imaging

- Advanced beamforming methods (p-DAS or Capon (TODO)), with a dedicated
  tutorial to understand how these are implemented and how to implement your
  own methods

- Basic Doppler methods (Color and Power maps), and their dedicated utilities
  functions (matched filtering, RF to I/Qs conversion)

- Advanced Doppler methods, such as Vector Doppler (TODO) or propositions for
  alias-free alias-free Doppler velocities (dual-wavelength method)

- Basic metrics for evaluation of the data quality (SNR), or of our beamforming
  algorithms (FWHM, PSL, CNR)


Documentation
=============
Full documentation can be found in the 'docs' folder, and is also available at
https://ultraspy.readthedocs.io/en/latest. You will find there all the detailed
information about how to install ultraspy and how to use it.


Installation
============
Installation can be easily done using pypi:

.. code-block:: console

    $ pip install ultraspy

Also, if you want to run it on GPU, you need to install the proper version of
`cupy` based on your CUDA version:

.. code-block:: console

    $ pip install cupy-cudaXXx


Contribute
==========

- Issue Tracker: https://gitlab.com/pecarlat/ultraspy/-/issues/

- Source Code: https://gitlab.com/pecarlat/ultraspy

- Documentation: https://ultraspy.readthedocs.io/en/latest


License
=======
The project is under the MIT license.
