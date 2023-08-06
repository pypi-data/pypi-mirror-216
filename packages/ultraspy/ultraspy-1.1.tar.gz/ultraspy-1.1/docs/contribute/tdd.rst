Test Driven Development
=======================

What are we talking about?
--------------------------
The tests ensure the stability of the code. Which is why those should not be
modified unless you are sure you've found a mistake in them.

However, it is a very good practice to adapt a Test-Driven Development process,
which consists in writing a test of your new method / algorithm before even
writing the said method. That way, you force yourself to think of how the
method should and shouldn't work, and also to think about the different
possible input and outputs.

.. warning::
    The TDD process hasn't been applied since the beginning of the lib
    development, which means that some of the current methods might not be
    tested. If you find any, feel free to add the dedicated tests.


:code:`tests/` repo
-------------------
The tests are using the :code:`pytest` lib, and are stored in the
:code:`tests/` repo. Basically, in our structure, we have:

- the :code:`tests/test_cpu/` repo contains all the tests of the CPU methods,
  plus the validation tests. Let's say for example if we want to compare the
  efficiency of the DAS algorithm with another ultrasound lib, most of the
  comparisons will be made here

- the :code:`tests/test_gpu/` repo contains all the tests of the GPU methods.
  Since most of the validation tests were already made within the CPU folder,
  we are mainly comparing the CPU and GPU results. If the GPU mode is equal to
  the CPU mode, we assume that the validation tests on CPU are also valid for
  the GPU mode.
