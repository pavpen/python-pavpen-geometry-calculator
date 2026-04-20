# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from pavpen.geometry_calculator.vector_field_implementations.tuple_vector_field_float_operations import (
    TupleVectorFieldFloatOperations,
)


class TestTupleVectorFieldFloatOperations:
    def test_additive_identity_is_identity(self):
        # Setup
        vector_field_operations = TupleVectorFieldFloatOperations.for_1d()

        # Act, and verify
        assert vector_field_operations.additive_identity == (0,)

    def test_added_returns_a_sum(self):
        # Setup
        vector_field_operations = TupleVectorFieldFloatOperations.for_2d()

        # Act, and verify
        assert vector_field_operations.added((7, 5), (3, 2)) == (10, 7)

    def test_scaled_scales(self):
        # Setup
        vector_field_operations = TupleVectorFieldFloatOperations.for_3d()

        # Act, and verify
        assert vector_field_operations.scaled((3, 2, 7), 5) == (15, 10, 35)

    def test_inner_multiplied_returns_an_inner_product(self):
        # Setup
        vector_field_operations = TupleVectorFieldFloatOperations.for_2d()

        # Act, and verify
        assert vector_field_operations.inner_multiplied((3, 2), (4, 5)) == 22
