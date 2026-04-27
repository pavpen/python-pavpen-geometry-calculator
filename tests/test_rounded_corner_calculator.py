# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import math
from dataclasses import dataclass
from typing import cast

import pytest

from pavpen.geometry_calculator.faults import (
    AmbiguousComputationDueToPrecisionWarning,
    ImpossibleOutputGeometryError,
)
from pavpen.geometry_calculator.rounded_corner_calculator import RoundedCornerCalculator
from pavpen.geometry_calculator.vector_field_implementations.tuple_float_vector_field_operations import (
    TupleFloatVectorFieldOperations,
)


@dataclass
class CalculateTestCase:
    id: str
    vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
    radius: float
    expected_center: tuple[float, float]
    expected_arc_start: tuple[float, float]
    expected_arc_midpoint: tuple[float, float]
    expected_arc_end: tuple[float, float]
    x_hat: tuple[float, float] = (1, 0)
    y_hat: tuple[float, float] = (0, 1)
    float_tolerance: float = 1e-8


class TestRoundedCornerCalculator:
    @pytest.mark.parametrize(
        "test_case",
        [
            CalculateTestCase(
                id="┘-corner, quadrant 2 arc",
                vertices=((0, 0), (4, 0), (4, 4)),
                radius=1,
                expected_center=(3, 1),
                expected_arc_start=(3, 0),
                expected_arc_end=(4, 1),
                expected_arc_midpoint=(3 + 1 / math.sqrt(2), 1 - 1 / math.sqrt(2)),
            ),
            CalculateTestCase(
                id="┐-corner, quadrant 3 arc",
                vertices=((4, 0), (4, 4), (0, 4)),
                radius=1,
                expected_center=(3, 3),
                expected_arc_start=(4, 3),
                expected_arc_end=(3, 4),
                expected_arc_midpoint=(3 + 1 / math.sqrt(2), 3 + 1 / math.sqrt(2)),
            ),
            CalculateTestCase(
                id="└-corner, quadrant 1 arc",
                vertices=((0, 4), (0, 0), (4, 0)),
                radius=1,
                expected_center=(1, 1),
                expected_arc_start=(0, 1),
                expected_arc_end=(1, 0),
                expected_arc_midpoint=(1 - 1 / math.sqrt(2), 1 - 1 / math.sqrt(2)),
            ),
            CalculateTestCase(
                id="┌-corner, quadrant 4 arc",
                vertices=((0, 0), (0, 4), (4, 4)),
                radius=1,
                expected_center=(1, 3),
                expected_arc_start=(0, 3),
                expected_arc_end=(1, 4),
                expected_arc_midpoint=(1 - 1 / math.sqrt(2), 3 + 1 / math.sqrt(2)),
            ),
            CalculateTestCase(
                id="Clockwise ┘-corner arc",
                vertices=((4, 4), (4, 0), (0, 0)),
                radius=1,
                expected_center=(3, 1),
                expected_arc_start=(4, 1),
                expected_arc_end=(3, 0),
                expected_arc_midpoint=(3 + 1 / math.sqrt(2), 1 - 1 / math.sqrt(2)),
            ),
        ],
        ids=lambda test_case: test_case.id,
    )
    def test_calculate_result_matches_a_test_case(self, test_case: CalculateTestCase) -> None:
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_2d()
        calculator = RoundedCornerCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=test_case.float_tolerance,
            previous_vertex=test_case.vertices[0],
            corner_vertex=test_case.vertices[1],
            next_vertex=test_case.vertices[2],
            radius=test_case.radius,
            x_hat=test_case.x_hat,
            y_hat=test_case.y_hat,
        )

        # Act
        result = calculator.calculate()

        # Verify
        assert result.x_hat == pytest.approx(test_case.x_hat)
        assert result.y_hat == pytest.approx(test_case.y_hat)
        assert result.center == pytest.approx(test_case.expected_center)
        assert result.radius == pytest.approx(test_case.radius)
        assert result.arc_start == pytest.approx(test_case.expected_arc_start)
        assert result.arc_midpoint == pytest.approx(test_case.expected_arc_midpoint)
        assert result.arc_end == pytest.approx(test_case.expected_arc_end)

    def test_calculate_reports_a_warning_on_ambiguous_center_location(self) -> None:
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_2d()
        calculator = RoundedCornerCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            previous_vertex=(0, 0),
            corner_vertex=(0, 4),
            next_vertex=(0, 8),
            radius=1,
            x_hat=(1, 0),
            y_hat=(0, 1),
        )

        # Act
        with pytest.warns(AmbiguousComputationDueToPrecisionWarning) as warnings:
            result = calculator.calculate()

        # Verify
        assert result.x_hat == pytest.approx((1, 0))
        assert result.y_hat == pytest.approx((0, 1))
        # This is an unstable solution.  The center could easily be at (-1, 4)
        # as well:
        assert result.center == pytest.approx((1, 4))
        assert result.radius == pytest.approx(1)
        assert result.arc_start == pytest.approx((0, 4))
        assert result.arc_midpoint == pytest.approx((0, 4))
        assert result.arc_end == pytest.approx((0, 4))

        assert len(warnings) == 1
        warning = cast("AmbiguousComputationDueToPrecisionWarning", warnings[0].message)
        assert warning.ambiguous_value_names == ["RoundedCornerCalculator.center"]
        assert warning.tolerance == pytest.approx(1e-8)
        assert warning.difference_from_alternate_solution == pytest.approx(0)
        assert warning.causing_exception is None

    def test_calculate_throws_on_previous_vertex_inside_arc_circle(self) -> None:
        """
        ```
                      ^
                      |
                      |   * (4, 4) previous_vertex
                      |
                  *---+---*-->
                (-4, 0)  (4, 0)
            next_vertex   corner_vertex
        ```
        """

        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_2d()
        calculator = RoundedCornerCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            previous_vertex=(4, 4),
            corner_vertex=(4, 0),
            next_vertex=(-4, 0),
            radius=5,
            x_hat=(1, 0),
            y_hat=(0, 1),
        )

        # Act and verify
        with pytest.raises(
            ImpossibleOutputGeometryError,
            match=(
                r"Rounded corner previous vertex is within the corner part "
                "cut off by rounding the corner."
            ),
        ):
            calculator.calculate()

    def test_calculate_throws_on_next_vertex_inside_arc_circle(self) -> None:
        """
        ```
                      ^
                      |
                      |   * (4, 8) previous_vertex
                      |
                      |
                      *---*-->
                 (0, 0)   (4, 0)
            next_vertex   corner_vertex
        ```
        """

        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_2d()
        calculator = RoundedCornerCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            previous_vertex=(4, 8),
            corner_vertex=(4, 0),
            next_vertex=(0, 0),
            radius=5,
            x_hat=(1, 0),
            y_hat=(0, 1),
        )

        # Act and verify
        with pytest.raises(
            ImpossibleOutputGeometryError,
            match=(
                r"Rounded corner next vertex is within the corner part "
                "cut off by rounding the corner."
            ),
        ):
            calculator.calculate()

    def test_calculate_chooses_a_plane_basis_if_unspecified(self) -> None:
        # Setup
        vector_field_operations = TupleFloatVectorFieldOperations.for_2d()
        calculator = RoundedCornerCalculator(
            vector_field_operations=vector_field_operations,
            float_tolerance=1e-8,
            previous_vertex=(0, 0),
            corner_vertex=(4, 0),
            next_vertex=(4, 4),
            radius=1,
        )

        # Act
        result = calculator.calculate()

        # Verify
        assert result.x_hat == pytest.approx((1, 0))
        assert result.y_hat == pytest.approx((0, 1))

        assert result.center == pytest.approx((3, 1))
        assert result.radius == pytest.approx(1)
        assert result.arc_start == pytest.approx((3, 0))
        assert result.arc_midpoint == pytest.approx((3 + math.sqrt(2) / 2, 1 - math.sqrt(2) / 2))
        assert result.arc_end == pytest.approx((4, 1))
