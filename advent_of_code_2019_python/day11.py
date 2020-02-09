from collections import defaultdict, namedtuple

import click

from advent_of_code_2019_python import IntcodeComputer


Position = namedtuple('Position', ['x', 'y'])


def turn_left(x, y):
    return -y, x


def turn_right(x, y):
    return y, -x


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day11.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    colors = defaultdict(int)
    position = Position(x=0, y=0)
    dx = 0
    dy = 1

    painted_panels = set()

    while not intcode_computer.halted:
        intcode_computer.set_inputs(colors[position])
        color = intcode_computer.compute()
        colors[position] = color
        painted_panels.add(position)
        direction = intcode_computer.compute()
        dx, dy = turn_right(dx, dy) if direction else turn_left(dx, dy)
        position = Position(position.x + dx, position.y + dy)

    print(f'Panels painted at least once: {len(painted_panels)}')


if __name__ == '__main__':
    main()
