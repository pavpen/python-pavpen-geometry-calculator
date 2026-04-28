# Geometry Calculator

[![Measure test coverage](https://github.com/pavpen/python-pavpen-geometry-calculator/actions/workflows/measure-test-coverage.yaml/badge.svg?event=push)](https://github.com/pavpen/python-pavpen-geometry-calculator/actions/workflows/measure-test-coverage.yaml)
[![Code coverage report](https://raw.githubusercontent.com/wiki/pavpen/python-pavpen-geometry-calculator/status/tests/reports/codecov-badge.svg)](https://github.com/pavpen/python-pavpen-geometry-calculator/wiki/coverage#test-coverage)

Calculate coordinates, and other elements of a collection of geometric
constructions.

-----

## Table of Contents

* [Example](#example)
* [Installation](#installation)
* [License](#license)
* [Documentation](#documentation)

## Example

```python
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

```

### Notes

* Algebraic operations are separate from the objects storing vectors.  This
  allows treating existing objects as vectors without having to modify their
  inheritance hierarchy, or wrap them.
  * In the above example `TupleFloatVectorFieldOperations.for_3d()` returns an
    object which treats a `tuple[float, float, float]` as a 3-dimensional
    orthonormal vector.

## Installation

```console
pip install pavpen-geometry-calculator
```

## License

Geometry Calculator is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.

## Documentation

See the
[API documentation site](https://pavpen.github.io/python-pavpen-geometry-calculator/).
