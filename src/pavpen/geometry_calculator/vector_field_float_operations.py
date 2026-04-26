# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import math

from pavpen.geometry_calculator.vector_field_operations import VectorFieldOperations


class VectorFieldFloatOperations[Vector](VectorFieldOperations[float, Vector]):
    """Base class for
    :py:class:`~pavpen.geometry_calculator.vector_field_operations.VectorFieldOperations`
    whose coordinates are :py:class:`float`\\ s

    Knowing the type of the coordinates allows us to provide default
    implementations for some properties, and methods.
    """

    @property
    def multiplicative_negator(self) -> float:
        return -1

    def norm(self, value: Vector) -> float:
        return math.sqrt(self.inner_multiplied(value, value))

    def normalized(self, value: Vector) -> Vector:
        return self.scaled(value, 1.0 / self.norm(value))

    def projection_length_on(self, projected: Vector, direction: Vector) -> float:
        return self.inner_multiplied(projected, direction) / self.norm(direction)
