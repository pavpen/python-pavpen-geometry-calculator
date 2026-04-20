# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from pavpen.geometry_calculator.vector_field_implementations.complex_vector_field_operations import (
    ComplexVectorFieldOperations,
)


class TestComplexVectorFieldOperations:
    def test_additive_identity_is_identity(self):
        # Setup
        vector_field_operations = ComplexVectorFieldOperations()

        # Act, and verify
        assert vector_field_operations.additive_identity + (3 + 2j) == 3 + 2j

    def test_added_returns_a_sum(self):
        # Setup
        vector_field_operations = ComplexVectorFieldOperations()

        # Act, and verify
        assert vector_field_operations.added((7 + 5j), (3 + 2j)) == 10 + 7j

    def test_scaled_scales(self):
        # Setup
        vector_field_operations = ComplexVectorFieldOperations()

        # Act, and verify
        assert vector_field_operations.scaled(3 + 2j, 5) == 15 + 10j

    def test_inner_multiplied_returns_an_inner_product(self):
        # Setup
        vector_field_operations = ComplexVectorFieldOperations()

        # Act, and verify
        assert vector_field_operations.inner_multiplied(3 + 2j, 4 + 5j) == 22
