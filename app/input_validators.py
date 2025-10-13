from __future__ import annotations
from typing import Sequence, Tuple, List
from .exceptions import ValidationError

def parse_numbers(args: Sequence[str]) -> List[float]:
    nums: List[float] = []
    for a in args:
        try:
            nums.append(float(a))
        except ValueError as e:
            raise ValidationError(f"invalid number '{a}'") from e
    return nums

def parse_command(line: str) -> Tuple[str, List[str]]:
    if not line:
        return ("", [])
    parts = line.strip().split()
    return (parts[0].lower(), parts[1:])
