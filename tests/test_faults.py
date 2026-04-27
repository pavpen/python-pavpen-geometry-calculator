from pavpen.geometry_calculator.faults import CalculationPrecisionExceededError


class TestCalculationPrecisionExceededError:
    def test_value_name_is_included_in_message(self):
        # Act
        result = CalculationPrecisionExceededError(tolerance=1, calculation_error=2, value_name="test_calculated_value")

        # Verify
        assert "'test_calculated_value'" in str(result)
        assert "tolerance (1)" in str(result)
        assert "(calculation error: 2)" in str(result)

    def test_can_construct_without_value_name(self):
        # Act
        result = CalculationPrecisionExceededError(tolerance=2, calculation_error=3)

        # Verify
        assert "tolerance (2)" in str(result)
        assert "(calculation error: 3)" in str(result)
