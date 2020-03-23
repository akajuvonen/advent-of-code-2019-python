from typing import List, Tuple

import click
import numpy as np  # type: ignore

from advent_of_code_2019_python.intcode_computer import IntcodeComputer


def populate_array(intcode_computer: IntcodeComputer) -> np.ndarray:
    array: List[List[int]] = []
    i = 0
    array.append([])
    output = intcode_computer.compute()
    while not intcode_computer.halted:
        if output == 10:
            array.append([])
            i += 1
        else:
            array[i].append(output)
        output = intcode_computer.compute()
    # The program outputs a couple of empty lines at the end, let's clear the resulting empty lists
    while not array[-1]:
        array.pop()
    return np.array(array)


def get_intersections(array: np.ndarray) -> List[Tuple[int, int]]:
    intersections = []
    rows, cols = array.shape
    for i in range(rows):
        for j in range(cols):
            if _is_intersection((i, j), array):
                intersections.append((i, j))
    return intersections


def _is_intersection(location: Tuple, array: np.ndarray) -> bool:
    row, col = location
    surrounding_locations = [(row, col - 1), (row, col + 1), (row + 1, col), (row - 1, col)]
    try:
        for n, m in surrounding_locations:
            if not array[n][m] == 35:
                return False
    except IndexError:
        return False
    return True


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day17.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    scaffolds_array = populate_array(intcode_computer)

    # Converts ints to ascii characters when printing
    np.set_printoptions(formatter={'all': lambda x: chr(x)}, threshold=np.inf, linewidth=120)
    print(scaffolds_array)

    intersections = get_intersections(scaffolds_array)
    sum_of_alignment_params = sum([i[0] * i[1] for i in intersections])
    print(f'Sum of alignment parameters: {sum_of_alignment_params}')


if __name__ == '__main__':
    main()
