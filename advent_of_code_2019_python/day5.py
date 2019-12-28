from advent_of_code_2019_python import intcode_computer

import click


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day5.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode = intcode_computer.read_input(input_file)
    intcode_computer.compute_intcode(intcode=intcode, input_value=1)


if __name__ == '__main__':
    main()
