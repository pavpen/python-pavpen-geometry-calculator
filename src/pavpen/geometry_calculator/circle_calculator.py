# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import logging
import math

from pavpen.geometry_calculator.vector_field_float_operations import VectorFieldFloatOperations

logger = logging.getLogger(__name__)


class CircleCalculator[Vector]:
    """Calculates the location of points on a circle (or an ellipse, if the
    norms of `x_hat`, and `y_hat` are different)

    Example:

    >>> import math
    >>> from pavpen.geometry_calculator.vector_field_implementations.tuple_vector_field_float_operations import (
    ...     TupleVectorFieldFloatOperations,
    ... )
    >>>
    >>> CircleCalculator(
    ...     vector_field_operations=TupleVectorFieldFloatOperations.for_2d(),
    ...     center=(0, 0),
    ...     radius=1,
    ...     x_hat=(1, 0),
    ...     y_hat=(0, 1),
    ... ).point_at_angle_rad(math.pi / 4)
    (0.7071067811865476, 0.7071067811865476)
    """

    def __init__(
        self,
        vector_field_operations: VectorFieldFloatOperations[Vector],
        center: Vector,
        radius: float,
        x_hat: Vector | None = None,
        y_hat: Vector | None = None,
    ):
        self.vector_field_operations = vector_field_operations
        self.center = center
        self.radius = radius
        self._x_hat = vector_field_operations.additive_identity if x_hat is None else x_hat
        self._y_hat = vector_field_operations.additive_identity if y_hat is None else y_hat

    def point_at_angle_rad(self, angle_rad: float) -> Vector:
        vec = self.vector_field_operations
        x_offset = vec.scaled(self._x_hat, self.radius * math.cos(angle_rad))
        y_offset = vec.scaled(self._y_hat, self.radius * math.sin(angle_rad))

        return vec.summed(self.center, x_offset, y_offset)
