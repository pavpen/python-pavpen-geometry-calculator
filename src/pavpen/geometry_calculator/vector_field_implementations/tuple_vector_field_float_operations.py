# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from typing import cast

from pavpen.geometry_calculator.float_vector_field_operations import FloatVectorFieldOperations


class TupleVectorFieldFloatOperations[Vector: tuple[float, ...]](FloatVectorFieldOperations[Vector]):
    """Treats tuples of floats as vectors in an orthonormal space"""

    @staticmethod
    def for_1d() -> "TupleVectorFieldFloatOperations[tuple[float]]":
        return TupleVectorFieldFloatOperations[tuple[float]](component_count=1)

    @staticmethod
    def for_2d() -> "TupleVectorFieldFloatOperations[tuple[float, float]]":
        return TupleVectorFieldFloatOperations[tuple[float, float]](component_count=2)

    @staticmethod
    def for_3d() -> "TupleVectorFieldFloatOperations[tuple[float, float,float]]":
        return TupleVectorFieldFloatOperations[tuple[float, float, float]](component_count=3)

    def __init__(self, component_count: int) -> None:
        super().__init__()
        self._component_count = component_count

    @property
    def additive_identity(self) -> Vector:
        return cast("Vector", (0,) * self._component_count)

    def added(self, addend1: Vector, addend2: Vector) -> Vector:
        return cast(
            "Vector",
            tuple(coordinate1 + coordinate2 for coordinate1, coordinate2 in zip(addend1, addend2, strict=False)),
        )

    def scaled(self, multiplicand: Vector, scalar: float) -> Vector:
        return cast("Vector", tuple(coordinate * scalar for coordinate in multiplicand))

    def inner_multiplied(self, multiplicand1: Vector, multiplicand2: Vector) -> float:
        return sum(
            coordinate1 * coordinate2 for coordinate1, coordinate2 in zip(multiplicand1, multiplicand2, strict=False)
        )
