# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import pytest

from pavpen.geometry_calculator.vector_field_operations import VectorFieldOperations


class UnimplementedVectorFieldOperations[Scalar, Vector](VectorFieldOperations[Scalar, Vector]):
    @property
    def additive_identity(self) -> Vector:
        return super().additive_identity

    @property
    def multiplicative_negator(self) -> Scalar:
        return super().multiplicative_negator

    def negated(self, value: Vector) -> Vector:
        return self.scaled(value, self.multiplicative_negator)

    def added(self, addend1: Vector, addend2: Vector) -> Vector:
        return super().added(addend1, addend2)

    def subtracted(self, diminuend: Vector, subtrahend: Vector) -> Vector:
        return self.added(diminuend, self.negated(subtrahend))

    def scaled(self, multiplicand: Vector, scalar: Scalar) -> Vector:
        return super().scaled(multiplicand=multiplicand, scalar=scalar)

    def inner_multiplied(self, multiplicand1: Vector, multiplicand2: Vector) -> Scalar:
        return super().inner_multiplied(multiplicand1, multiplicand2)

    def norm(self, value: Vector) -> Scalar:
        return super().norm(value)

    def normalized(self, value: Vector) -> Vector:
        return super().normalized(value)

    def projection_length_on(self, projected: Vector, direction: Vector) -> Scalar:
        return super().projection_length_on(projected=projected, direction=direction)


class TestVectorFieldOperationsDefaultImplementations:
    """Tests the default implementations in [VectorFieldOperations],
    to which [UnimplementedVectorFieldOperations] forwards method calls

    Also, code coverage include tests, so we test our
    [UnimplementedVectorFieldOperations] helper class.  (See the tip in
    [Exclude code from test coverage](https://python-basics-tutorial.readthedocs.io/en/latest/test/pytest/coverage.html#exclude-code-from-test-coverage).)
    """

    def test_additive_identity_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            _ = operations.additive_identity

    def test_multiplicative_negator_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            _ = operations.multiplicative_negator

    def test_added_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            operations.added(3 + 4j, 5 + 6j)

    def test_scaled_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            operations.scaled(3 + 4j, 7)

    def test_inner_multiplied_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            operations.inner_multiplied(3 + 4j, 7 + 8j)

    def test_norm_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            operations.norm(7 + 8j)

    def test_normalized_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            operations.normalized(7 + 8j)

    def test_projection_length_on_throws(self):
        # Setup
        operations = UnimplementedVectorFieldOperations[float, complex]()

        # Act, and verify
        with pytest.raises(NotImplementedError):
            operations.projection_length_on(7 + 8j, 9 + 10j)


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
