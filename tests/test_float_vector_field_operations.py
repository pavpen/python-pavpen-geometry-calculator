# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import pytest

from pavpen.geometry_calculator.float_vector_field_operations import FloatVectorFieldOperations


class UnimplementedFloatVectorFieldOperations[Vector](FloatVectorFieldOperations[Vector]):
    @property
    def additive_identity(self) -> Vector:
        raise NotImplementedError

    def negated(self, value: Vector) -> Vector:
        return self.scaled(value, self.multiplicative_negator)

    def added(self, addend1: Vector, addend2: Vector) -> Vector:
        raise NotImplementedError

    def subtracted(self, diminuend: Vector, subtrahend: Vector) -> Vector:
        return self.added(diminuend, self.negated(subtrahend))

    def scaled(self, multiplicand: Vector, scalar: float) -> Vector:
        raise NotImplementedError

    def inner_multiplied(self, multiplicand1: Vector, multiplicand2: Vector) -> float:
        raise NotImplementedError


class TestFloatVectorFieldOperations:
    def test_norm_returns_a_value_corresponding_to_inner_product(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedFloatVectorFieldOperations[tuple[float, float]]):
            def inner_multiplied(self, multiplicand1: tuple[float, float], multiplicand2: tuple[float, float]) -> float:
                return multiplicand1[0] * multiplicand2[0] + multiplicand1[1] * multiplicand2[1]

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.norm((3, 4)) == pytest.approx(5)

    def test_normalized_returns_a_unit_vector(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedFloatVectorFieldOperations[tuple[float, float]]):
            def scaled(self, multiplicand: tuple[float, float], scalar: float) -> tuple[float, float]:
                return (multiplicand[0] * scalar, multiplicand[1] * scalar)

            def inner_multiplied(self, multiplicand1: tuple[float, float], multiplicand2: tuple[float, float]) -> float:
                return multiplicand1[0] * multiplicand2[0] + multiplicand1[1] * multiplicand2[1]

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.normalized((3, -4)) == pytest.approx((3.0 / 5.0, -4.0 / 5.0))

    def test_projection_length_on_calculates_a_positive_length(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedFloatVectorFieldOperations[tuple[float, float]]):
            def inner_multiplied(self, multiplicand1: tuple[float, float], multiplicand2: tuple[float, float]) -> float:
                return multiplicand1[0] * multiplicand2[0] + multiplicand1[1] * multiplicand2[1]

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.projection_length_on((3, 4), (0, 1)) == pytest.approx(4)

    def test_projection_length_on_calculates_a_negative_length(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedFloatVectorFieldOperations[tuple[float, float]]):
            def inner_multiplied(self, multiplicand1: tuple[float, float], multiplicand2: tuple[float, float]) -> float:
                return multiplicand1[0] * multiplicand2[0] + multiplicand1[1] * multiplicand2[1]

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.projection_length_on((3, 4), (0, -1)) == pytest.approx(-4)
