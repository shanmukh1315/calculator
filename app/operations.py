from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, Dict, Type
from .exceptions import OperationError, ValidationError

class OperationStrategy(ABC):
    name: str

    @abstractmethod
    def execute(self, numbers: Sequence[float]) -> float:
        ...

class Add(OperationStrategy):
    name = "add"
    def execute(self, numbers: Sequence[float]) -> float:
        return float(sum(numbers))

class Subtract(OperationStrategy):
    name = "sub"
    def execute(self, numbers: Sequence[float]) -> float:
        if not numbers:
            raise ValidationError("sub requires at least one number")
        total = numbers[0]
        for n in numbers[1:]:
            total -= n
        return float(total)

class Multiply(OperationStrategy):
    name = "mul"
    def execute(self, numbers: Sequence[float]) -> float:
        total = 1.0
        for n in numbers:
            total *= n
        return float(total)

class Divide(OperationStrategy):
    name = "div"
    def execute(self, numbers: Sequence[float]) -> float:
        if not numbers:
            raise ValidationError("div requires at least one number")
        total = numbers[0]
        for n in numbers[1:]:
            if n == 0:
                raise OperationError("division by zero")
            total /= n
        return float(total)

class Power(OperationStrategy):
    name = "pow"
    def execute(self, numbers: Sequence[float]) -> float:
        if len(numbers) != 2:
            raise ValidationError("pow requires exactly two numbers (base exponent)")
        base, exp = numbers
        return float(base ** exp)

class Root(OperationStrategy):
    name = "root"
    def execute(self, numbers: Sequence[float]) -> float:
        if len(numbers) != 2:
            raise ValidationError("root requires exactly two numbers (value degree)")
        value, degree = numbers
        if degree == 0:
            raise OperationError("root degree cannot be zero")
        if value < 0 and degree % 2 == 0:
            raise OperationError("even root of negative value not supported")
        return float(value ** (1.0 / degree))

_FACTORY: Dict[str, Type[OperationStrategy]] = {
    Add.name: Add,
    Subtract.name: Subtract,
    Multiply.name: Multiply,
    Divide.name: Divide,
    Power.name: Power,
    Root.name: Root,
}

def make_operation(name: str) -> OperationStrategy:
    key = name.strip().lower()
    try:
        return _FACTORY[key]()
    except KeyError:
        raise ValidationError(f"unknown operation '{name}'. Supported: {', '.join(sorted(_FACTORY))}")
