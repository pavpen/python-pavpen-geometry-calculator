# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT


class CalculationPrecisionExceededError(ValueError):
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
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AmbiguousComputationDueToPrecisionWarning(RuntimeWarning):
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
