import click
from typing import List, Tuple, Set


def read_input(filename: str) -> Tuple[List[str], List[str]]:
    with open(filename) as f:
        wire_a, wire_b = f.read().rstrip('\n').split('\n')
    return wire_a.split(','), wire_b.split(',')


def wire_path_to_set(paths: List[str]) -> Set[Tuple[int, int]]:
    points = set()
    xy = (0, 0)
    for path in paths:
        direction = path[0]
        steps = int(path[1:])
        if direction == 'R':
            movement = (1, 0)
        elif direction == 'L':
            movement = (-1, 0)
        elif direction == 'U':
            movement = (0, 1)
        elif direction == 'D':
            movement = (0, -1)
        else:
            raise ValueError('Unexpected direction {direction}')
        for i in range(steps):
            xy = (xy[0] + movement[0], xy[1] + movement[1])
            points.add(xy)
    return points



@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day3.txt', show_default=True,
              help='Path to file containing wire paths (AoC Day3 input.txt)')
def main(input_file):
    wire_a_paths, wire_b_paths = read_input(input_file)
    wire_a_points = wire_path_to_set(wire_a_paths)
    wire_b_points = wire_path_to_set(wire_b_paths)
    intersections = wire_a_points.intersection(wire_b_points)


if __name__ == '__main__':
    main()
