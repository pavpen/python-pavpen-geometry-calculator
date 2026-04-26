# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod


class VectorFieldOperations[Scalar, Vector](ABC):
    """Provides an implementation of vector operations for a given data type
    which can be interpreted as storing vectors

    Having this as a separate object allows decoupling the data type storing
    vectors from an implementation of vector operations (such as addition,
    scaling, norm).  This, in turn, allows us to treat existing data objects
    (e.g., tuples) as vectors without having to patch their data type's
    algebraic operations (e.g., a tuple multiplied by a scalar is already
    defined), which may break other code relying on them, or adding a wrapper
    type, which may introduce the need for marshalling.
    """

    @property
    @abstractmethod
    def additive_identity(self) -> Vector:
        """The 'zero' vector, i.e. `x`, such that for any vector `v`:
        `x + v = v`
        """

        ...

    @property
    @abstractmethod
    def multiplicative_negator(self) -> Scalar:
        """The '-1' scalar, i.e. `x`, such that for any vector (or scalar) `v`:
        `v * x + v = 0`
        """

        ...

    def negated(self, value: Vector) -> Vector:
        return self.scaled(value, self.multiplicative_negator)

    @abstractmethod
    def added(self, addend1: Vector, addend2: Vector) -> Vector:
        """Return the vector sum of `addend1`, and `addend2`"""

        ...

    def summed(self, addend1: Vector, *rest_addends: Vector) -> Vector:
        result = addend1
        for addend in rest_addends:
            result = self.added(result, addend)

        return result

    def subtracted(self, diminuend: Vector, subtrahend: Vector) -> Vector:
        return self.added(diminuend, self.negated(subtrahend))

    @abstractmethod
    def scaled(self, multiplicand: Vector, scalar: Scalar) -> Vector:
        """Returns `multiplicand` scaled (multiplied) by `scalar`"""

        ...

    @abstractmethod
    def inner_multiplied(self, multiplicand1: Vector, multiplicand2: Vector) -> Scalar:
        """Returns the inner product of `multiplicand1`, and `multiplicand2`

        In an orthonormal basis, this is the same as the dot (component-wise)
        product.  In either case, the result of the inner product must be the
        product of the norms of each multiplicand, and of the orthogonal
        projection of one multiplicand on the other (the result being negative,
        if the projeciton endpoint is in the opposite direction of the vector).
        """

        ...

    @abstractmethod
    def norm(self, value: Vector) -> Scalar: ...

    @abstractmethod
    def normalized(self, value: Vector) -> Vector: ...

    @abstractmethod
    def projection_length_on(self, projected: Vector, direction: Vector) -> Scalar:
        """The norm of the component of the projection of *projected* on
        *direction*
        """

        ...
