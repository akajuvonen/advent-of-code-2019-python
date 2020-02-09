import click

from advent_of_code_2019_python import IntcodeComputer


def print_outputs(intcode_computer: IntcodeComputer):
    while not intcode_computer.halted:
        output = intcode_computer.compute()
        if output is not None:
            print(output)


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day9.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    intcode_computer.set_inputs(1)
    print_outputs(intcode_computer)

    intcode_computer = IntcodeComputer.from_file(input_file)
    intcode_computer.set_inputs(2)
    print_outputs(intcode_computer)


if __name__ == '__main__':
    main()
