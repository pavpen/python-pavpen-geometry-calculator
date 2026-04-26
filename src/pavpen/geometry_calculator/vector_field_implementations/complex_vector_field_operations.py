# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from pavpen.geometry_calculator.float_vector_field_operations import FloatVectorFieldOperations


class ComplexVectorFieldOperations(FloatVectorFieldOperations[complex]):
    """Treats complex numbers as 2-D vectors"""

    @property
    def additive_identity(self) -> complex:
        return 0 + 0j

    def added(self, addend1: complex, addend2: complex) -> complex:
        return addend1 + addend2

    def scaled(self, multiplicand: complex, scalar: float) -> complex:
        return multiplicand * scalar

    def inner_multiplied(self, multiplicand1: complex, multiplicand2: complex) -> float:
        return multiplicand1.real * multiplicand2.real + multiplicand1.imag * multiplicand2.imag
