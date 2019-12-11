import click
from typing import List, Tuple, Generator, Set


def read_input(filename: str) -> Tuple[List[str], List[str]]:
    with open(filename) as f:
        wire_a, wire_b = f.read().rstrip('\n').split('\n')
    return wire_a.split(','), wire_b.split(',')


def calculate_path(paths: List[str]) -> Generator[Tuple[int, int], None, None]:
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
            yield xy


def manhattan_distance_from_origin(x: int, y: int) -> int:
    return abs(x) + abs(y)


def min_distance(wire_a_points, wire_b_points):
    intersections = set(wire_a_points).intersection(set(wire_b_points))
    return min([manhattan_distance_from_origin(intersection[0], intersection[1]) for intersection in intersections])


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day3.txt', show_default=True,
              help='Path to file containing wire paths (AoC Day3 input.txt)')
def main(input_file):
    wire_a_paths, wire_b_paths = read_input(input_file)
    wire_a_points = [path for path in calculate_path(wire_a_paths)]
    wire_b_points = [path for path in calculate_path(wire_b_paths)]

    distance = min_distance(wire_a_points, wire_b_points)
    print(f'Minimum intersection distance: {distance}')


if __name__ == '__main__':
    main()
