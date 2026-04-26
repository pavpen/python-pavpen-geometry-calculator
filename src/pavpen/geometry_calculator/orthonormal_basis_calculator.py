# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from typing import Self

from pavpen.geometry_calculator.defaults import DEFAULT_TOLERANCE
from pavpen.geometry_calculator.faults import CalculationPrecisionExceededError
from pavpen.geometry_calculator.vector_field_float_operations import VectorFieldFloatOperations


class OrthonormalBasisCalculator[Vector]:
    """Calculates an orthonormal basis of a space that spans a given set of
    points

    Example:

    >>> import math
    >>> from pavpen.geometry_calculator import OrthonormalBasisCalculator
    >>> from pavpen.geometry_calculator.vector_field_implementations import (
    ...     TupleVectorFieldFloatOperations,
    ... )
    >>>
    >>> OrthonormalBasisCalculator(
    ...     vector_field_operations=TupleVectorFieldFloatOperations.for_3d(),
    ...     float_tolerance=1e-8,
    ...     points=((0, 0, 0), (0, 2, 0), (0, 0, -2)),
    ... ).calculate().basis_vectors
    [(0.0, 1.0, 0.0), (0.0, 0.0, -1.0)]
    """

    def __init__(
        self,
        vector_field_operations: VectorFieldFloatOperations[Vector],
        points: list[Vector],
        float_tolerance: float = DEFAULT_TOLERANCE,
    ) -> None:
        self._vector_field_operations = vector_field_operations
        self._points = points
        if len(points) < 1:
            message = f"The `points` argument must contain, at least, one element.  len(points): {len(points)}"
            raise ValueError(message)
        self._float_tolerance = float_tolerance

    def calculate(self, *, require_points_are_non_redundant: bool = False) -> Self:
        """Calculates, and sets `self.basis_vectors: List[Vector]`

        The values in `basis_vectors` are orthonormal vectors spanning the
        space that contains the `points` passed in during construction.  Two
        non-redundant points define a line, three points define a plane, etc.

        Setting `require_points_are_non_redundant` to `True` makes it an
        exception for `points` to be spanned by less than `len(points) - 1`
        basis vectors.  In this case [CalculationPrecisionExceededError] is
        raised, if two points are too close to each other, or if two different
        pairs of points define directions that are close to colinear, or if a
        computation's maximum tolerance exceeds `float_tolerance` (specified
        during object construction) for any other reason.
        """

        points = self._points
        try:
            [first_point, *rest_points] = points
        except ValueError as e:
            e.add_note(
                f"The `points` collection in "
                f"{OrthonormalBasisCalculator.__name__} must contain, at "
                f"least one element.  len(points): {len(points)}"
            )
            raise
        vec = self._vector_field_operations
        basis_vectors: list[Vector] = []
        for point in rest_points:
            non_spanned_component = vec.subtracted(point, first_point)
            for basis_vector in basis_vectors:
                projection_on_basis_vector_size = vec.inner_multiplied(non_spanned_component, basis_vector)
                projection_on_basis_vector = vec.scaled(basis_vector, projection_on_basis_vector_size)
                non_spanned_component = vec.subtracted(non_spanned_component, projection_on_basis_vector)
            non_spanned_component_norm = vec.norm(non_spanned_component)
            if non_spanned_component_norm < self._float_tolerance:
                if require_points_are_non_redundant:
                    raise CalculationPrecisionExceededError(
                        tolerance=self._float_tolerance,
                        calculation_error=float("inf"),
                        value_name="non_spanned_component_norm",
                    )
            else:
                basis_vectors.append(vec.scaled(non_spanned_component, 1 / non_spanned_component_norm))

        self.basis_vectors = basis_vectors

        return self
