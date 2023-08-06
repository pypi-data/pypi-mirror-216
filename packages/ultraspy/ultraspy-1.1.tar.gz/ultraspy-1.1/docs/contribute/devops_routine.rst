DevOps routine
==============

What are we talking about?
--------------------------
As specified earlier, it is important to test the code before pushing any
new feature. The DevOps routine is all the procedures that have been set in
order to ensure the security and non-regression of the code.


Git
---
The master branch is protected, so you need to create your own branch to add
your works. Make sure to give your branch an explicit name with what feature
you want to include, and try to use a specific branch for each small feature,
this will make it easier to test and maintain. Once the changes are finished,
you can create a merge request that will be validated by one of the maintainer
of the code.

.. warning::
    Note that the tox routine is not part of the DevOps, so you need to ensure
    that you've run the tests beforehand. In the future, the merge to the
    master branch should automatically run the tests on a dedicated server.


Build and upload
----------------
Once the feature has been added into the master branch, you might want to
update the `ultraspy` package on pypi. The first thing you need to do is to
update the current version of the project in `setup.py`, so the build will
have the proper version. Also, it is a good practice to add the update within
the `CHANGELOG.rst` file with the new version and a list of the new features
implemented.

Once this is done, you need to build the sources into a distribution so it can
be uploaded in a release server, such as pypi.

::

    python -m build

The newly built wheel is now in the dist/ directory. The next step is then to
upload it:

::

    python -m twine upload --skip-existing dist/ultraspy*

The last thing to do would be to build the documentation. If you ran tox, it
should already be available in the dist/docs directory. You can check it out
locally to make sure it matches your expectations. Then you can connect to
https://readthedocs.org/ and build the latest version of the package.
