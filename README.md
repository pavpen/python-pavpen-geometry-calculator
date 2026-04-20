# Geometry Calculator

Calculate coordinates, and other elements of a collection of geometric
constructions.

-----

## Table of Contents

* [Example](#example)
* [Install](#install)
* [License](#license)

## Example

```python
# Calculates an orthonormal basis of a space that spans a given set of
# points

import math
from pavpen.geometry_calculator.vector_field_implementations.tuple_vector_field_float_operations import (
    TupleVectorFieldFloatOperations,
)

result = OrthonormalBasisCalculator(
    vector_field_operations=TupleVectorFieldFloatOperations.for_3d(),
    float_tolerance=1e-8,
    points=((0, 0, 0), (0, 2, 0), (0, 0, -2)),
).calculate().basis_vectors

assert result == [(0.0, 1.0, 0.0), (0.0, 0.0, -1.0)]
```

### Notes

* Algebraic operations are separate from the objects storing vectors.  This
  allows treating existing objects as vectors without having to modify their
  inheritance hierarchy, or wrap them.
  * In the above example `TupleVectorFieldFloatOperations.for_3d()` returns an
    object which treats a `tuple[float, float, float]` as a 3-dimensional
    orthonormal vector.

## Install

```console
pip install pavpen-geometry-calculator
```

## License

Geometry Calculator is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
