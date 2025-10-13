import pytest
from app.input_validators import parse_numbers, parse_command
from app.exceptions import ValidationError

def test_parse_numbers_ok():
    assert parse_numbers(["1", "2.5"]) == [1.0, 2.5]

def test_parse_numbers_bad():
    with pytest.raises(ValidationError):
        parse_numbers(["a"])

def test_parse_command():
    cmd, args = parse_command("add 1 2 3")
    assert cmd == "add" and args == ["1", "2", "3"]

def test_parse_command_empty():
    cmd, args = parse_command("")
    assert cmd == "" and args == []
