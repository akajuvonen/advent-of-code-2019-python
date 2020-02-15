import click

from advent_of_code_2019_python import IntcodeComputer

import numpy as np

def _array_formatter(x):
    icons = {1: '#',
             2: 'X',
             3: '_',
             4: 'O'}
    return icons[x] if x in icons else '.'


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
        if x is not None and y is not None:
            tiles[(x, y)] = tile
    print(f' Number of block tiles on the screen: {list(tiles.values()).count(2)}')

    max_x, max_y = 0, 0
    for x, y in tiles:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    screen = np.zeros((max_y + 1, max_x + 1), dtype=np.int8) 
    for x, y in tiles:
        screen[y][x] = tiles[(x, y)]
    np.set_printoptions(formatter={'all': _array_formatter}, linewidth=100)
    print(screen)

if __name__ == '__main__':
    main()
