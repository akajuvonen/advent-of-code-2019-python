import pytest

from advent_of_code_2019_python import IntcodeComputer


@pytest.mark.parametrize('intcode, expected',
                         [([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
                          ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
                          ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
                          ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])])
def test_compute(intcode, expected):
    assert IntcodeComputer.compute(intcode) == expected


def test_input():
    input = 1
    intcode = [3, 0, 99]
    expected = [1, 0, 99]
    assert IntcodeComputer.compute(intcode=intcode, input=input) == expected


def test_output(capsys):
    intcode = [4, 0, 99]
    expected = 4
    IntcodeComputer.compute(intcode=intcode)
    captured = capsys.readouterr()
    assert captured.out.rstrip('\n') == str(expected)
