import os
import pandas as pd
import pytest
from app.history import History, COLUMNS
from app.calculation import Calculation
from datetime import datetime, UTC
from app.exceptions import ValidationError

def test_history_add_and_snapshot(tmp_path):
    path = tmp_path / "h.csv"
    h = History(autosave=False, path=str(path), ts_format="%Y")
    c = Calculation(op="add", numbers=[1,2], result=3.0, ts=datetime.now(UTC))
    h.add(c)
    assert list(h.df.columns) == COLUMNS
    snap = h.to_snapshot()
    h.clear()
    h.restore(snap)
    assert len(h.df) == 1

def test_history_persistence(tmp_path):
    path = tmp_path / "h.csv"
    h = History(autosave=True, path=str(path), ts_format="%Y")
    c = Calculation(op="add", numbers=[1], result=1.0, ts=datetime.now(UTC))
    h.add(c)
    assert os.path.exists(path)
    h2 = History(autosave=False, path=str(path), ts_format="%Y")
    assert len(h2.df) == 1

def test_history_load_file_not_found_silent(tmp_path):
    path = tmp_path / "missing.csv"
    h = History(autosave=False, path=str(path), ts_format="%Y")
    assert list(h.df.columns) == COLUMNS and len(h.df) == 0

def test_history_load_empty_file(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("")
    h = History(autosave=False, path=str(path), ts_format="%Y")
    assert list(h.df.columns) == COLUMNS and len(h.df) == 0

def test_history_load_bad_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"bad": [1]}).to_csv(path, index=False)
    with pytest.raises(ValidationError):
        History(autosave=False, path=str(path), ts_format="%Y")

def test_history_load_missing_file_raises_when_not_silent(tmp_path):
    path = tmp_path / "nope.csv"
    h = History(autosave=False, path=str(path), ts_format="%Y")
    with pytest.raises(FileNotFoundError):
        h.load(silent=False)
