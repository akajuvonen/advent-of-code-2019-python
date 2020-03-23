from advent_of_code_2019_python.intcode_computer import IntcodeComputer
import click


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day17.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    output = intcode_computer.compute()
    while not intcode_computer.halted:
        char = chr(output)
        print(char, end='')
        output = intcode_computer.compute()


if __name__ == '__main__':
    main()
