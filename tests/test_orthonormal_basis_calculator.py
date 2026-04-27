# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import math
from typing import cast

import pytest

from pavpen.geometry_calculator.faults import CalculationPrecisionExceededError
from pavpen.geometry_calculator.orthonormal_basis_calculator import OrthonormalBasisCalculator
from pavpen.geometry_calculator.vector_field_implementations.tuple_float_vector_field_operations import (
    TupleFloatVectorFieldOperations,
)


class TestOrthonormalBasisCalculator:
    def test_constructor_throws_on_empty_points_collection(self):
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_1d()

        # Act, and verify
        with pytest.raises(ValueError, match=r"The `points` argument must contain at least one element."):
            OrthonormalBasisCalculator(
                vector_field_operations=vector_field_operations,
                float_tolerance=1e-8,
                points=[],
            )

    def test_calculate_throws_on_empty_points_collection(self):
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_1d()
        points = [(3.0,)]
        calculator = OrthonormalBasisCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            points=points,
        )

        # Act, and verify
        points.clear()
        with pytest.raises(
            ValueError,
            match=r"The `points` collection in OrthonormalBasisCalculator must contain at least one element.",
        ):
            calculator.calculate()

    def test_calculate_throws_on_redundant_points(self):
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_3d()
        calculator = OrthonormalBasisCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            points=[(0, 0, 0), (0, 0, -1), (0, 0, 1)],
        )

        # Act, and verify
        with pytest.raises(CalculationPrecisionExceededError) as exc_info:
            calculator.calculate(require_points_are_non_redundant=True)

        # Verify
        exception = cast("CalculationPrecisionExceededError", exc_info.value)
        assert exception.tolerance == pytest.approx(1e-8)
        assert exception.calculation_error == float("inf")
        assert exception.value_name == "non_spanned_component_norm"

    def test_calculate_ignores_redundant_points(self):
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_3d()
        calculator = OrthonormalBasisCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            points=[(0, 0, 0), (0, 0, -1), (0, 0, 1)],
        )

        # Act
        basis_vectors = calculator.calculate(require_points_are_non_redundant=False).basis_vectors

        # Verify
        assert len(basis_vectors) == 1
        assert basis_vectors[0] == pytest.approx((0, 0, -1))

    def test_calculate_returns_an_orthonormal_basis(self):
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_3d()
        calculator = OrthonormalBasisCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            points=[(1, 1, 1), (1, 1, -1), (0, 0, 0)],
        )

        # Act
        basis_vectors = calculator.calculate(require_points_are_non_redundant=True).basis_vectors

        # Verify
        assert len(basis_vectors) == 2
        assert basis_vectors[0] == pytest.approx((0, 0, -1))
        assert basis_vectors[1] == pytest.approx((-1.0 / math.sqrt(2), -1.0 / math.sqrt(2), 0))
