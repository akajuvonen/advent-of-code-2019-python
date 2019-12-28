import pytest

from advent_of_code_2019_python import intcode_computer


@pytest.mark.parametrize('intcode, expected',
                         [([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
                          ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
                          ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
                          ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])])
def test_compute(intcode, expected):
    assert intcode_computer.compute_intcode(intcode) == expected


def test_input():
    input_value = 1
    intcode = [3, 0, 99]
    expected = [1, 0, 99]
    assert intcode_computer.compute_intcode(intcode=intcode, input_value=input_value) == expected


def test_output(capsys):
    intcode = [4, 0, 99]
    expected = intcode[0]
    intcode_computer.compute_intcode(intcode=intcode)
    captured = capsys.readouterr()
    assert captured.out.rstrip('\n') == str(expected)


def test_immediatemode():
    intcode = [1002, 4, 3, 4, 33]
    expected = [1002, 4, 3, 4, 99]
    assert intcode_computer.compute_intcode(intcode=intcode) == expected
