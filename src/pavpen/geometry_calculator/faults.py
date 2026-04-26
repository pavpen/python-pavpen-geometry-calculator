# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT


class CalculationPrecisionExceededError(ValueError):
    """Raised when a computation in algorithm step exceeds the maximum allowed
    calculation error (floating point tolerance)

    For example, if you try to normalize a vector whose norm is sufficiently
    close to zero using float operations, the result may be a vector whose
    coordinates have 1 significant digit, or compute as infinite.
    """

    def __init__(self, tolerance: float, calculation_error: float, value_name: str | None = None) -> None:
        self._tolerance = tolerance
        self._calculation_error = calculation_error
        self._value_name = value_name
        message = f"Maximum calculation tolerance ({tolerance}) exceeded (calculation error: {calculation_error})"
        if value_name is not None:
            message += f" for value {value_name!r}"
        message += "!"
        super().__init__(message)

    @property
    def tolerance(self) -> float:
        """Maximum numerical error in caculation approximations

        This is the value that was exceeded in the exception.
        """

        return self._tolerance

    @property
    def calculation_error(self) -> float:
        """The numerical error in the calculation that caused this exception"""

        return self._calculation_error

    @property
    def value_name(self) -> str | None:
        """Name of the value whose calculation exceeded the calculation
        tolerance
        """

        return self._value_name


class ImpossibleOutputGeometryError(ValueError):
    """Raised when the output of a calculation is physically impossible

    E.g., a line with a negative length, a sphere with a negative radius, etc.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class AmbiguousComputationDueToPrecisionWarning(RuntimeWarning):
    """Raised when a calculation may produce more than possible output (e.g.,
    having the center of an output circle on one side of a given line, or the
    other), but the calculation failed to unambiguously distinguish which of
    the possible alternatives to return, because the difference between the
    distinguishing factors is within the calculation error (floating point
    tolerance).

    As an example of such a calculation, you can consider determining the
    the point, diametrically opposite the second of 3 input points, which
    define the circle.  If none of the 3 input points coincide, but they lie on
    a line, the radius of the circle becomes infinite, and there are two
    solutions, one on each side of the line, on a perpendicular to the second
    of the 3 input points.

    If the 3 input points given to the calculation are on a line, or
    sufficiently close to a line (within the floating point tolerance), the
    calculation may return one of the possible results, but raise this warning,
    because the other possible solution, is also within the floating point
    tolerance of the input.
    """

    def __init__(
        self,
        ambiguous_value_names: list[str],
        tolerance: float,
        difference_from_alternate_solution: float,
        causing_exception: Exception | None = None,
    ):
        """
        :param ambiguous_value_names: List of variables whose computed values
        are ambigous due to computation precision.  Each name in the list can be in the form "object.name", e.g. "RoundedCornerCalculator.center".
        """

        suffix = "" if causing_exception is None else f"\nCaused by: {causing_exception}"
        message = (
            f"{self.__class__.__name__}: The solution was ambiguous while "
            f"computing values {ambiguous_value_names!r} because the difference "
            f"from an alternate solution "
            f"({difference_from_alternate_solution}) < the computational "
            f"tolerance ({tolerance}){suffix}"
        )
        super().__init__(message)
        self.ambiguous_value_names = ambiguous_value_names
        self.tolerance = tolerance
        self.difference_from_alternate_solution = difference_from_alternate_solution
        self.causing_exception = causing_exception
