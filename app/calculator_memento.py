from __future__ import annotations
from typing import List, Optional
from .history import History, HistorySnapshot

class Caretaker:
    def __init__(self, capacity: int = 100):
        self._undo: List[HistorySnapshot] = []
        self._redo: List[HistorySnapshot] = []
        self.capacity = capacity

    def save(self, history: History) -> None:
        snap = history.to_snapshot()
        self._undo.append(snap)
        if len(self._undo) > self.capacity:
            self._undo.pop(0)
        self._redo.clear()

    def undo(self) -> Optional[HistorySnapshot]:
        if not self._undo:
            return None
        snap = self._undo.pop()
        self._redo.append(snap)
        return snap

    def redo(self) -> Optional[HistorySnapshot]:
        if not self._redo:
            return None
        return self._redo.pop()
