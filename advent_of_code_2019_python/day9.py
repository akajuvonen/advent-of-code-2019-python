import click

from advent_of_code_2019_python import IntcodeComputer


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day9.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    intcode_computer.set_inputs(1)
    intcode_computer.compute()
    while not intcode_computer.halted:
        print(intcode_computer.output)
        intcode_computer.compute()


if __name__ == '__main__':
    main()
