import click

from advent_of_code_2019_python import IntcodeComputer


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day5.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    print('Air conditioner unit test output (ID: 1)')
    intcode_computer = IntcodeComputer.from_file(input_file)
    intcode_computer.compute(input_value=1)
    while not intcode_computer.halted:
        print(intcode_computer.output)
        intcode_computer.compute()

    intcode_computer.reset()

    print('Thermal radiator controller test output (ID: 5)')
    intcode_computer.compute(input_value=5)
    print(intcode_computer.output)


if __name__ == '__main__':
    main()
