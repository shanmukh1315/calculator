import pytest
from app.operations import make_operation, Add, Subtract, Multiply, Divide, Power, Root
from app.exceptions import ValidationError, OperationError

@pytest.mark.parametrize("op,nums,expected", [
    ("add", [1,2,3], 6.0),
    ("sub", [10,3,2], 5.0),
    ("mul", [2,3,4], 24.0),
    ("div", [20,2,2], 5.0),
    ("pow", [2,3], 8.0),
    ("root", [27,3], 3.0),
])
def test_strategies_happy(op, nums, expected):
    strat = make_operation(op)
    assert pytest.approx(strat.execute(nums), rel=1e-9) == expected

def test_division_by_zero():
    with pytest.raises(OperationError):
        Divide().execute([4, 0])

@pytest.mark.parametrize("op,nums", [
    ("pow", [2]),
    ("root", [9]),
    ("root", [9, 0]),
])
def test_validation_errors(op, nums):
    strat = make_operation(op)
    with pytest.raises((ValidationError, OperationError)):
        strat.execute(nums)

def test_unknown_operation():
    with pytest.raises(ValidationError):
        make_operation("noop")

def test_subtract_requires_args():
    with pytest.raises(ValidationError):
        Subtract().execute([])

def test_divide_requires_args():
    with pytest.raises(ValidationError):
        Divide().execute([])

def test_root_even_degree_negative_value():
    with pytest.raises(OperationError):
        Root().execute([-8, 2])
