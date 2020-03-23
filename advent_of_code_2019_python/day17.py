import click
import numpy as np

from advent_of_code_2019_python.intcode_computer import IntcodeComputer


def print_array(array: np.ndarray):
    np.set_printoptions(formatter={'all': lambda x: chr(x)}, threshold=np.inf, linewidth=120)
    print(array)


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day17.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    scaffolds = []
    i = 0
    scaffolds.append([])
    output = intcode_computer.compute()
    while not intcode_computer.halted:
        if output == 10:
            scaffolds.append([])
            i += 1
        else:
            scaffolds[i].append(output)
        output = intcode_computer.compute()
    # The program outputs a couple of empty lines at the end, let's clear the resulting empty lists
    while not scaffolds[-1]:
        scaffolds.pop()
    scaffolds_array = np.array(scaffolds)
    print_array(scaffolds_array)


if __name__ == '__main__':
    main()
