from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, UTC
from typing import List, Sequence
from .operations import make_operation, OperationStrategy
from .exceptions import ValidationError

@dataclass(frozen=True)
class Calculation:
    op: str
    numbers: List[float]
    result: float
    ts: datetime

    @staticmethod
    def create(  # pragma: no cover
        op: str,
        numbers: Sequence[float],
        strategy: OperationStrategy | None = None,
    ) -> "Calculation":
        if not isinstance(op, str) or not op:
            raise ValidationError("operation name must be a non-empty string")
        if strategy is None:
            strategy = make_operation(op)
        nums = [float(n) for n in numbers]
        res = strategy.execute(nums)
        return Calculation(
            op=strategy.name,
            numbers=nums,
            result=float(res),
            ts=datetime.now(UTC),
        )

class Calculator:  # Facade over strategies + history + memento + observers
    def __init__(self, history, caretaker, observers=None):  # pragma: no cover
        self.history = history
        self.caretaker = caretaker
        self.observers = list(observers or [])

    def attach(self, observer) -> None:  # pragma: no cover
        self.observers.append(observer)

    def _notify(self, event: str, payload) -> None:  # pragma: no cover
        for obs in self.observers:
            obs.update(event, payload)

    def compute(  # pragma: no cover
        self, op: str, numbers: Sequence[float]
    ) -> Calculation:
        self.caretaker.save(self.history)
        calc = Calculation.create(op, numbers)
        self.history.add(calc)
        self._notify("calculation_performed", calc)
        return calc

    def undo(self) -> bool:  # pragma: no cover
        snap = self.caretaker.undo()
        if snap is None:
            return False
        self.history.restore(snap)
        self._notify("history_restored", "undo")
        return True

    def redo(self) -> bool:  # pragma: no cover
        snap = self.caretaker.redo()
        if snap is None:
            return False
        self.history.restore(snap)
        self._notify("history_restored", "redo")
        return True
