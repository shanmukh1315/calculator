class CalculatorError(Exception):
    """Base exception for calculator errors."""


class ConfigurationError(CalculatorError):
    """Raised for configuration issues."""


class ValidationError(CalculatorError):
    """Raised when user input or data is invalid."""


class OperationError(CalculatorError):
    """Raised when an operation cannot be performed."""
