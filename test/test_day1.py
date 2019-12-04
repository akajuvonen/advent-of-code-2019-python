import pytest

from advent_of_code_2019_python.day1 import calculate_fuel, calculate_total_fuel


@pytest.mark.parametrize('mass, fuel', [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
def test_calculate_fuel(mass, fuel):
    assert calculate_fuel(mass) == fuel


@pytest.mark.parametrize('mass, total_fuel', [(14, 2), (1969, 966), (100756, 50346)])
def test_calculate_total_fuel(mass, total_fuel):
    assert calculate_total_fuel(mass) == total_fuel
