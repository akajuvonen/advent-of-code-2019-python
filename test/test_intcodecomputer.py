import pytest

from advent_of_code_2019_python import IntcodeComputer


@pytest.mark.parametrize('intcode, expected',
                         [([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
                          ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
                          ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
                          ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])])
def test_compute(intcode, expected):
    intcode_computer = IntcodeComputer(intcode)
    intcode_computer.compute()
    assert intcode_computer.intcode == expected


def test_input():
    input_value = 1
    intcode = [3, 0, 99]
    expected = [1, 0, 99]
    intcode_computer = IntcodeComputer(intcode)
    intcode_computer.compute(input_value=input_value)
    assert intcode_computer.intcode == expected


def test_output():
    input_value = -1
    intcode = [3, 0, 4, 0, 99]
    intcode_computer = IntcodeComputer(intcode)
    intcode_computer.compute(input_value=input_value)
    assert intcode_computer.output == input_value


def test_immediatemode():
    intcode = [1002, 4, 3, 4, 33]
    expected = [1002, 4, 3, 4, 99]
    intcode_computer = IntcodeComputer(intcode)
    intcode_computer.compute()
    assert intcode_computer.intcode == expected


@pytest.mark.parametrize('intcode', [([1005, 2, 5, -15, -16, 99]), ([1106, 0, 5, -12, -13, 99])])
def test_jump_instructions(intcode):
    intcode_computer = IntcodeComputer(intcode)
    intcode_computer.compute()


@pytest.mark.parametrize('intcode, expected', [([1107, 1, 2, 0, 99], [1, 1, 2, 0, 99]),
                                               ([1108, 1, 1, 0, 99], [1, 1, 1, 0, 99])])
def test_comparisons(intcode, expected):
    intcode_computer = IntcodeComputer(intcode)
    intcode_computer.compute()
    assert intcode_computer.intcode == expected
