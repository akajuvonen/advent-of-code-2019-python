import pytest

from advent_of_code_2019_python.day1 import calculate_fuel


@pytest.mark.parametrize('weight, fuel', [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
def test_calculate_fuel(weight, fuel):
    assert calculate_fuel(weight) == fuel
