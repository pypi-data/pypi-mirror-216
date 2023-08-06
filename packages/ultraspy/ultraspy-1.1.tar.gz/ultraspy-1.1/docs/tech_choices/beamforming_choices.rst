Miscellaneous choices in beamforming
====================================

Interpolation
-------------
In the equation (2) of the :ref:`Delay And Sum algorithm<das_algo>`, we’re
using the time delays to know which time sample to pick in our data. However,
the ultrasound data is discrete, and we might need to do interpolation to
interpret our delays. Thus, the choice of the interpolation method is
important. In order to choose, we’ve tried a few on Picmus data using the DAS
algorithm, and we’ve pictured the results in figure below. It’s been observed
that an interpolation method is mandatory, as the figure a is really noisy.
However, we also can notice that the linear interpolation method (figure b) is
offering quite good results and, even if cubic or quadratic interpolations are
slightly better, they also take longer to compute, so we’ve decided they are
irrelevant for our algorithms.

.. image:: ../images/interpolation_beamforming.png
   :width: 800


f-number and aperture
---------------------
Something important to consider when we are computing our vector of delays is
the aperture of the probe elements. Indeed, each element has a physical
aperture, which is defined by the probe specifications, and it means that not
every element can “see” the whole medium we’re scanning. Considering this, we
can simplify the calculations by ignoring elements outside of the directivity
of one element, as shown in figure below. The aperture might not be known, so
we are using a variable called f# (f-number) to define it. We define it based
on depth: :math:`f\#=\frac{z}{\text{aperture}(z)}`. Practically, for each pixel
of the scan X=(x,z), we’re defining :math:`q_{n,m}(x,z)` to zero if
:math:`|x-x_{n}|\leq\frac{z}{2.f\#}`. Literally, we’re making sure that the
distance between an element and X in the lateral axe is superior to twice the
aperture. When we increase f#, :math:`alpha` is decreasing, so if f# is set to
0, we suppose that every element is seeing everything (:math:`alpha=90\deg`).
In our case, we often use f#=1.75 (20°), but it is left free to define to the
user.

Considering this, we also need to define how we are dealing with the borders.
Indeed, when working with pixels outside of the range of the probe, we’ll have
undefined values in the vector of delays. This can be dealt by (1) never
beamform pixels out of bound, (2) pad the data by zero values, or (3) put the
out of bound values of the vector to zero. We are doing the latest.

.. image:: ../images/fnumber.png
   :width: 300
   :align: center


TODO: Add how we deal with convex

TODO: Add emitted_aperture option

TODO: Add 2D f# when done


Delay And Sum... or Mean?
-------------------------
In DAS, as its name states, we are summing the vector of delays for the
reduction step. This works in practice, but since we are setting f#>0, every
pixel will have a different number of elements to reduce depending on its depth
(the deeper we go, the more probe elements are concerned, as shown in Figure
above). Thus, if we are summing the vector of delays, it will give more
importance to the deepest diffractors. An alternative can be to reduce the
vector of delays by doing its average instead of its sum, which would normalize
the beamformed values by the number of elements concerned at every location of
the medium. The difference is shown in Figure 7, with an example on Picmus
dataset.

.. image:: ../images/das_dam.png
   :width: 400
   :align: center


TODO: This is why DAM affects the compound / reduce options


Apodization
-----------
TODO: Explain the tukey window depending on f#
