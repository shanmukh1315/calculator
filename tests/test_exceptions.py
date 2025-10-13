from app.exceptions import CalculatorError, ConfigurationError, ValidationError, OperationError

def test_exception_hierarchy():
    for ex in (ConfigurationError, ValidationError, OperationError):
        assert issubclass(ex, CalculatorError)
