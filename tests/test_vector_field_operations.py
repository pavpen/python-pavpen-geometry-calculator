# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from pavpen.geometry_calculator.vector_field_operations import VectorFieldOperations


class UnimplementedVectorFieldOperations[Scalar, Vector](VectorFieldOperations[Scalar, Vector]):
    @property
    def additive_identity(self) -> Vector:
        raise NotImplementedError

    @property
    def multiplicative_negator(self) -> Scalar:
        raise NotImplementedError

    def negated(self, value: Vector) -> Vector:
        return self.scaled(value, self.multiplicative_negator)

    def added(self, addend1: Vector, addend2: Vector) -> Vector:
        raise NotImplementedError

    def subtracted(self, diminuend: Vector, subtrahend: Vector) -> Vector:
        return self.added(diminuend, self.negated(subtrahend))

    def scaled(self, multiplicand: Vector, scalar: Scalar) -> Vector:
        raise NotImplementedError

    def inner_multiplied(self, multiplicand1: Vector, multiplicand2: Vector) -> Scalar:
        raise NotImplementedError

    def norm(self, value: Vector) -> Scalar:
        raise NotImplementedError

    def normalized(self, value: Vector) -> Vector:
        raise NotImplementedError

    def projection_length_on(self, projected: Vector, direction: Vector) -> Scalar:
        raise NotImplementedError


class TestVectorFieldOperations:
    def test_negated_is_equivalent_to_scaling_by_multiplicative_negator(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedVectorFieldOperations[int, tuple[int, int]]):
            @property
            def multiplicative_negator(self) -> int:
                return -1

            def scaled(self, multiplicand: tuple[int, int], scalar: int) -> tuple[int, int]:
                return (multiplicand[0] * scalar, multiplicand[1] * scalar)

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.negated((3, -2)) == ((-3, 2))

    def test_summed_is_equivalent_to_composing_added(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedVectorFieldOperations[int, tuple[int, int]]):
            def added(self, addend1: tuple[int, int], addend2: tuple[int, int]) -> tuple[int, int]:
                return (addend1[0] + addend2[0], addend1[1] + addend2[1])

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.summed((3, -2), (4, 5)) == ((7, 3))

    def test_substracted_is_equivalent_to_currying_added_and_negated(self):
        # Setup
        class SampleVectorFieldOperations(UnimplementedVectorFieldOperations[int, tuple[int, int]]):
            def negated(self, value: tuple[int, int]) -> tuple[int, int]:
                return (-value[0], -value[1])

            def added(self, addend1: tuple[int, int], addend2: tuple[int, int]) -> tuple[int, int]:
                return (addend1[0] + addend2[0], addend1[1] + addend2[1])

        vector_field_operations = SampleVectorFieldOperations()

        # Act and verify
        assert vector_field_operations.subtracted((3, -2), (4, 6)) == ((-1, -8))
