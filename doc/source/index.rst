.. pavpen-geometry-calculator documentation master file, created by
   sphinx-quickstart on Wed Apr 22 22:10:05 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Geometry Calculator
===================

Disparate utilities for calculating coordinates and other elements of
geometric constructions.

Further Sections
----------------

.. toctree::
   :maxdepth: 2

   api/index

Example
-------

What using this package may be like:

.. doctest::

   >>> # Calculate an orthonormal basis of a space that spans a given set of
   >>> # points
   >>>
   >>> import math
   >>> from pavpen.geometry_calculator import OrthonormalBasisCalculator
   >>> from pavpen.geometry_calculator.vector_field_implementations import (
   ...    TupleFloatVectorFieldOperations,
   ... )
   >>>
   >>> OrthonormalBasisCalculator(
   ...    vector_field_operations=TupleFloatVectorFieldOperations.for_3d(),
   ...    float_tolerance=1e-8,
   ...    points=((0, 0, 0), (0, 2, 0), (0, 0, -2)),
   ... ).calculate().basis_vectors
   [(0.0, 1.0, 0.0), (0.0, 0.0, -1.0)]

Notes
^^^^^

* Algebraic operations are separate from the objects storing vectors.  This
  allows treating existing objects as vectors without having to modify their
  inheritance hierarchy, or wrap them.

  * In the above example `TupleFloatVectorFieldOperations.for_3d()` returns an
    object which treats a `tuple[float, float, float]` as a 3-dimensional
    orthonormal vector.
  * The `points` argument is an example of using such tuples to specify the
    points, which the requested orthonormal basis should span.
  * The `basis_vectors` result also uses such tuples.

Installation
------------

Install from PyPI using your favorite Python package manager.  E.g.:

.. code-block:: console

   pip install pavpen-geometry-calculator
