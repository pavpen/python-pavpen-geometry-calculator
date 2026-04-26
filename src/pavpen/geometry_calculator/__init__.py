"""Disparate utilities for calculating coordinates and other elements of
geometric constructions

See the `. . ._calculator` sub-modules for each calculation utility.

Other sub-modules, such as :py:mod:`~pavpen.geometry_calculator.faults`, and
:py:mod:`~pavpen.geometry_calculator.defaults` contain the core code shared by
the various calculators.
"""

from typing import Final

from pavpen.geometry_calculator._version import __commit_id__ as commit_id
from pavpen.geometry_calculator._version import __version__ as version
from pavpen.geometry_calculator._version import __version_tuple__ as version_tuple
from pavpen.geometry_calculator.circle_calculator import CircleCalculator as CircleCalculator
from pavpen.geometry_calculator.float_vector_field_operations import (
    FloatVectorFieldOperations as FloatVectorFieldOperations,
)
from pavpen.geometry_calculator.orthonormal_basis_calculator import (
    OrthonormalBasisCalculator as OrthonormalBasisCalculator,
)
from pavpen.geometry_calculator.planar_rotation_direction import PlanarRotationDirection as PlanarRotationDirection
from pavpen.geometry_calculator.rounded_corner_calculator import RoundedCornerCalculator as RoundedCornerCalculator
from pavpen.geometry_calculator.rounded_corner_calculator import (
    RoundedCornerCalculatorComputedValueNames as RoundedCornerCalculatorComputedValueNames,
)
from pavpen.geometry_calculator.vector_field_operations import VectorFieldOperations as VectorFieldOperations

__version__: Final[str] = version
"""The module version string.

It may contain suffixes, such as ``".dev7+dirty"``.
"""

__version_tuple__: Final[tuple[int | str, ...] | None] = version_tuple
"""This module's version components as a tuple

* May include suffixes.
* May be undefined.
"""

__commit_id__: Final[str | None] = commit_id
"""May be undefined"""
