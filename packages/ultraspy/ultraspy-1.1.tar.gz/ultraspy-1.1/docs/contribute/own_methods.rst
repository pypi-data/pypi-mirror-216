Add your own research methods
=============================

CPU / GPU
---------
The :ref:`common methods<common_methods>` of `ultraspy` are implemented in both
CPU and GPU, respectively in the :code:`cpu/` and :code:`gpu/` directories. If
you aim to add your own research method, you should add it in both.


__init__.py
-----------
In order for your methods to be called, you can import it within the
:code:`ultraspy.__init__.py` code, so it will be possible to call it directly
from the `ultraspy` module. Similarly for the CPU methods, those should be
imported from the :code:`ultraspy.cpu.__init__.py`. Thus it'll be callable
using `ultraspy.cpu` module.
