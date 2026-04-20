# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import math

import pytest

from pavpen.geometry_calculator.circle_calculator import CircleCalculator
from pavpen.geometry_calculator.vector_field_implementations.tuple_vector_field_float_operations import (
    TupleVectorFieldFloatOperations,
)


class TestCircleCalculator:
    def test_point_at_angle_rad_returns_a_point(self):
        # Setup
        vector_field_operations = TupleVectorFieldFloatOperations.for_2d()
        calculator = CircleCalculator(
            vector_field_operations=vector_field_operations,
            center=(0, 0),
            radius=1,
            x_hat=(1, 0),
            y_hat=(0, 1),
        )

        # Act
        result = calculator.point_at_angle_rad(0)

        # Verify
        assert result == pytest.approx((1, 0))

    def test_point_at_angle_rad_accepts_a_negative_angle(self):
        # Setup
        vector_field_operations = TupleVectorFieldFloatOperations.for_3d()
        calculator = CircleCalculator(
            vector_field_operations=vector_field_operations,
            center=(1, 0, 0),
            radius=1,
            x_hat=(0, 1, 0),
            y_hat=(0, 0, 1),
        )

        # Act
        result = calculator.point_at_angle_rad(-math.pi / 4)

        # Verify
        assert result == pytest.approx((1, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)))
