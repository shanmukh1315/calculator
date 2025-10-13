from app.calculator_memento import Caretaker
from app.history import History
from app.calculation import Calculation
from datetime import datetime, UTC

def test_undo_redo(tmp_path):
    hist = History(autosave=False, path=str(tmp_path / "h.csv"), ts_format="%s")
    ct = Caretaker(capacity=2)
    ct.save(hist)
    c = Calculation(op="add", numbers=[1,2], result=3, ts=datetime.now(UTC))
    hist.add(c)
    ct.save(hist)
    assert ct.undo() is not None
    assert ct.redo() is not None

def test_undo_redo_empty_and_capacity(tmp_path):
    hist = History(autosave=False, path=str(tmp_path / "h2.csv"), ts_format="%Y")
    ct = Caretaker(capacity=2)
    assert ct.undo() is None
    assert ct.redo() is None
    from app.calculation import Calculation
    from datetime import datetime, UTC
    for _ in range(3):
        ct.save(hist)
        hist.add(Calculation(op="add", numbers=[1], result=1.0, ts=datetime.now(UTC)))
    assert ct.undo() is not None
