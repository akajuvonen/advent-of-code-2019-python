import click

from advent_of_code_2019_python import IntcodeComputer




@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day13.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    tiles = {}
    while not intcode_computer.halted:
        x = intcode_computer.compute()
        y = intcode_computer.compute()
        tile = intcode_computer.compute()
        tiles[(x, y)] = tile
    print(f' Number of block tiles on the screen: {list(tiles.values()).count(2)}')


if __name__ == '__main__':
    main()
