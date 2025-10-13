import pytest
from app.calculation import Calculation, Calculator
from app.operations import Add
from app.calculator_memento import Caretaker
from app.history import History
from app.exceptions import ValidationError

def test_calculation_create_default_strategy():
    c = Calculation.create("add", [1, 2, 3])
    assert c.op == "add" and c.result == 6.0 and c.numbers == [1.0, 2.0, 3.0]

def test_calculation_with_strategy_instance():
    c = Calculation.create("add", [5], strategy=Add())
    assert c.result == 5.0

def test_calculation_bad_op_empty_string():
    with pytest.raises(ValidationError):
        Calculation.create("", [1])

def test_calculation_bad_op_non_string():
    with pytest.raises(ValidationError):
        Calculation.create(123, [1])  # type: ignore[arg-type]

def test_calculation_numbers_cast_from_strings():
    # hits the list-comprehension cast inside Calculation.create (previously missed line)
    c = Calculation.create("add", ["1", "2.5"])
    assert c.numbers == [1.0, 2.5]
    assert c.result == 3.5


class _Spy:
    def __init__(self):
        self.events = []
    def update(self, event, payload):
        self.events.append(event)

def test_calculator_observer_and_undo_redo_paths(tmp_path):
    h1 = History(autosave=False, path=str(tmp_path / "h1.csv"), ts_format="%Y")
    ct1 = Caretaker()
    spy = _Spy()
    calc1 = Calculator(history=h1, caretaker=ct1, observers=[spy])

    c = calc1.compute("add", [1, 2])
    assert c.result == 3.0
    assert "calculation_performed" in spy.events
    assert calc1.undo() is True
    assert calc1.redo() is True

    h2 = History(autosave=False, path=str(tmp_path / "h2.csv"), ts_format="%Y")
    ct2 = Caretaker()
    calc2 = Calculator(history=h2, caretaker=ct2)
    assert calc2.undo() is False
    assert calc2.redo() is False
