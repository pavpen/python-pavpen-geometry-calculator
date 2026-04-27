# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import math
import warnings
from enum import Enum
from typing import Annotated, Self

from pavpen.geometry_calculator.circle_calculator import CircleCalculator
from pavpen.geometry_calculator.defaults import DEFAULT_TOLERANCE
from pavpen.geometry_calculator.faults import (
    AmbiguousComputationDueToPrecisionWarning,
    ImpossibleOutputGeometryError,
)
from pavpen.geometry_calculator.float_vector_field_operations import FloatVectorFieldOperations
from pavpen.geometry_calculator.orthonormal_basis_calculator import OrthonormalBasisCalculator


class RoundedCornerCalculatorComputedValueNames(Enum):
    CENTER = "center"
    RADIUS = "radius"
    ARC_START = "arc_start"
    ARC_MIDPOINT = "arc_midpoint"
    ARC_END = "arc_end"


class RoundedCornerCalculator[Vector]:
    """Calculates the parameters of a rounded corner's circular arc

    The non-rounded corner, for which a rounded corner arc is to be
    calculated is determined by *previous_vertex*, *corner_vertex*, and
    *next_vertex*.

    If *x_hat*, and *y_hat* are specified, they define the coordinate
    system basis for outputs, such as the center of the rouded corner
    circle, and the start and end point of the rounded corner arc.

    :param vector_field_operations: defines how to calculate vector
       operations for vectors, such as *previous_vertex*, *corner_vertex*, and
       *next_vertex*

    :param radius: the radius of the rounded corner's circle
    """

    def __init__(
        self,
        vector_field_operations: FloatVectorFieldOperations[Vector],
        previous_vertex: Vector,
        corner_vertex: Vector,
        next_vertex: Vector,
        radius: float,
        x_hat: Vector | None = None,
        y_hat: Vector | None = None,
        float_tolerance: float = DEFAULT_TOLERANCE,
    ) -> None:
        self._vector_field_operations = vector_field_operations
        self._float_tolerance = float_tolerance
        self._previous_vertex = previous_vertex
        self._corner_vertex = corner_vertex
        self._next_vertex = next_vertex
        self._radius = radius
        self._x_hat = x_hat
        self._y_hat = y_hat

    def _calculate_basis(self) -> None:
        """Sets ``self.x_hat``, and ``self.y_hat``"""

        x_hat = self._x_hat
        y_hat = self._y_hat
        if x_hat is None:
            basis_calculator = OrthonormalBasisCalculator(
                vector_field_operations=self._vector_field_operations,
                float_tolerance=self._float_tolerance,
                points=[self._previous_vertex, self._corner_vertex, self._next_vertex],
            ).calculate()
            self.x_hat = basis_calculator.basis_vectors[0]
        else:
            self.x_hat = x_hat
        if y_hat is None:
            basis_calculator = OrthonormalBasisCalculator(
                vector_field_operations=self._vector_field_operations,
                float_tolerance=self._float_tolerance,
                points=[self._previous_vertex, self._corner_vertex, self._next_vertex],
            ).calculate()
            self.y_hat = basis_calculator.basis_vectors[1]
        else:
            self.y_hat = y_hat

    def calculate(self) -> Self:
        """Calculates, and sets the folowing output parameters of the rounded
        corner arc as attributes of ``self``:

        * ``center``
        * ``radius``
        * ``arc_start``
        * ``arc_midpoint``
        * ``arc_end``
        """

        self._calculate_basis()
        vec = self._vector_field_operations
        float_tolerance = self._float_tolerance
        previous_vertex = self._previous_vertex
        corner_vertex = self._corner_vertex
        next_vertex = self._next_vertex
        radius = self._radius
        corner_to_previous_vertex_vector = vec.subtracted(previous_vertex, corner_vertex)
        corner_to_next_vertex_vector = vec.subtracted(next_vertex, corner_vertex)
        corner_to_previous_vertex_angle_rad = math.atan2(
            vec.projection_length_along(direction=self.y_hat, projected=corner_to_previous_vertex_vector),
            vec.projection_length_along(direction=self.x_hat, projected=corner_to_previous_vertex_vector),
        )
        corner_to_next_vertex_angle_rad = math.atan2(
            vec.projection_length_along(direction=self.y_hat, projected=corner_to_next_vertex_vector),
            vec.projection_length_along(direction=self.x_hat, projected=corner_to_next_vertex_vector),
        )

        edge_to_edge_angle_rad = math.fabs(corner_to_previous_vertex_angle_rad - corner_to_next_vertex_angle_rad)
        corner_to_center_angle_rad = (corner_to_previous_vertex_angle_rad + corner_to_next_vertex_angle_rad) / 2.0
        difference_from_alternate_solution = math.fabs(edge_to_edge_angle_rad - math.pi)
        if difference_from_alternate_solution < float_tolerance:
            warnings.warn(
                AmbiguousComputationDueToPrecisionWarning(
                    ambiguous_value_names=[
                        f"{self.__class__.__name__}.{RoundedCornerCalculatorComputedValueNames.CENTER.value}"
                    ],
                    tolerance=float_tolerance,
                    difference_from_alternate_solution=difference_from_alternate_solution,
                ),
                stacklevel=1,
            )
        if edge_to_edge_angle_rad > math.pi:
            corner_to_center_angle_rad += math.pi
            edge_to_edge_angle_rad = 2.0 * math.pi - edge_to_edge_angle_rad
        center_to_edge_angle_rad = edge_to_edge_angle_rad / 2.0
        corner_to_center_dir = vec.added(
            vec.scaled(self.x_hat, math.cos(corner_to_center_angle_rad)),
            vec.scaled(self.y_hat, math.sin(corner_to_center_angle_rad)),
        )
        corner_to_center_distance = radius / math.sin(center_to_edge_angle_rad)
        center = vec.added(self._corner_vertex, vec.scaled(corner_to_center_dir, corner_to_center_distance))
        circle_calculator = CircleCalculator(
            vector_field_operations=vec,
            center=center,
            radius=radius,
            x_hat=self.x_hat,
            y_hat=self.y_hat,
        )

        edge_to_corner_shortening: Annotated[
            float,
            """Distance cut off by rounding the corner along each edge that
            would end at the corner vertex, if there was no rounding""",
        ] = corner_to_center_distance * math.cos(center_to_edge_angle_rad)

        corner_to_previous_vertex_vector_norm = vec.norm(corner_to_previous_vertex_vector)
        if corner_to_previous_vertex_vector_norm < edge_to_corner_shortening:
            message = (
                f"Rounded corner previous vertex is within the corner part "
                f"cut off by rounding the corner.  Values: "
                f"previous_vertex: {previous_vertex}, "
                f"corner_vertex: {corner_vertex}, "
                f"next_vertex: {next_vertex}, radius: {radius}; "
                f"corner_to_previous_vertex_vector norm: {corner_to_previous_vertex_vector_norm} < "
                f"edge_to_corner_shortening: {edge_to_corner_shortening}"
            )
            raise ImpossibleOutputGeometryError(message)
        arc_start = vec.added(
            corner_vertex,
            vec.scaled(
                vec.normalized(corner_to_previous_vertex_vector),
                edge_to_corner_shortening,
            ),
        )

        corner_to_next_vertex_vector_norm = vec.norm(corner_to_next_vertex_vector)
        if corner_to_next_vertex_vector_norm < edge_to_corner_shortening:
            message = (
                f"Rounded corner next vertex is within the corner part "
                f"cut off by rounding the corner.  Values: "
                f"previous_vertex: {previous_vertex}, "
                f"corner_vertex: {corner_vertex}, "
                f"next_vertex: {next_vertex}, radius: {radius}; "
                f"corner_to_next_vertex_vector norm: {corner_to_next_vertex_vector_norm} < "
                f"edge_to_corner_shortening: {edge_to_corner_shortening}"
            )
            raise ImpossibleOutputGeometryError(message)
        arc_end = vec.added(
            corner_vertex,
            vec.scaled(
                vec.normalized(corner_to_next_vertex_vector),
                edge_to_corner_shortening,
            ),
        )
        arc_midpoint = circle_calculator.point_at_angle_rad(corner_to_center_angle_rad + math.pi)

        self.center = center
        self.radius = radius
        self.arc_start = arc_start
        self.arc_midpoint = arc_midpoint
        self.arc_end = arc_end

        return self
