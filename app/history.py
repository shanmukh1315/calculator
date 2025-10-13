from __future__ import annotations
import pandas as pd
from dataclasses import dataclass
from .exceptions import ValidationError

COLUMNS = ["ts", "op", "numbers", "result"]

@dataclass
class HistorySnapshot:
    json_split: str  # DataFrame serialized via orient='split'

class History:
    def __init__(self, autosave: bool, path: str, ts_format: str):
        self.autosave = autosave
        self.path = path
        self.ts_format = ts_format
        self._df = pd.DataFrame(columns=COLUMNS)
        self.load(silent=True)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def add(self, calculation) -> None:
        row = {
            "ts": calculation.ts.strftime(self.ts_format),
            "op": calculation.op,
            "numbers": calculation.numbers,
            "result": calculation.result,
        }
        self._df = pd.concat([self._df, pd.DataFrame([row])], ignore_index=True)
        if self.autosave:
            self.save()

    def clear(self) -> None:
        self._df = pd.DataFrame(columns=COLUMNS)

    def to_snapshot(self) -> HistorySnapshot:
        return HistorySnapshot(json_split=self._df.to_json(orient="split"))

    def restore(self, snapshot: HistorySnapshot) -> None:
        self._df = pd.read_json(snapshot.json_split, orient="split")

    def save(self) -> None:
        self._df.to_csv(self.path, index=False)

    def load(self, silent: bool = False) -> None:
        try:
            self._df = pd.read_csv(self.path)
            if list(self._df.columns) != COLUMNS:
                raise ValidationError("history file has unexpected columns")
        except FileNotFoundError:
            if not silent:
                raise
        except pd.errors.EmptyDataError:
            self._df = pd.DataFrame(columns=COLUMNS)

class LoggingObserver:
    """Simple observer used in tests and REPL."""
    def __init__(self, sink=print):
        self.sink = sink
    def update(self, event: str, payload) -> None:
        self.sink(f"[observer] {event}: {payload}")  # pragma: no cover (visual/logging)
