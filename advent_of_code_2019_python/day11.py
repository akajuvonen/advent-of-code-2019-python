from collections import defaultdict, namedtuple
from typing import Dict, Tuple

import click

from advent_of_code_2019_python import IntcodeComputer
import numpy as np

Position = namedtuple('Position', ['x', 'y'])


def paint_panels(intcode_computer: IntcodeComputer, initial_color: int) -> Dict[Position, int]:
    colors: Dict[Position, int] = defaultdict(int)
    position = Position(x=0, y=0)
    dx = 0
    dy = 1
    colors[position] = initial_color

    while not intcode_computer.halted:
        intcode_computer.set_inputs(colors[position])
        color = intcode_computer.compute()
        if color is not None:
            colors[position] = color
        direction = intcode_computer.compute()
        dx, dy = turn_right(dx, dy) if direction else turn_left(dx, dy)
        position = Position(position.x + dx, position.y + dy)

    return colors


def turn_left(x: int, y: int) -> Tuple[int, int]:
    """Rotate a vector counter clockwise."""
    return -y, x


def turn_right(x: int, y: int) -> Tuple[int, int]:
    """Rotate a vector clockwise."""
    return y, -x


def generate_image(panels):
    xs = []
    ys = []
    for panel in panels:
        xs.append(panel.x)
        ys.append(-panel.y)
    image = np.zeros((max(ys) + 1, max(xs) + 1), dtype=np.int8)
    for panel in panels:
        image[-panel.y][panel.x] = panels[panel]
    return image



@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day11.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    painted_panels = paint_panels(intcode_computer, 0)
    print(f'Panels painted at least once: {len(painted_panels)}')

    intcode_computer = IntcodeComputer.from_file(input_file)
    painted_panels = paint_panels(intcode_computer, 1)
    np.set_printoptions(formatter={'all': lambda x: '#' if x == 1 else '.'}, linewidth=100)
    print(generate_image(painted_panels))

if __name__ == '__main__':
    main()
