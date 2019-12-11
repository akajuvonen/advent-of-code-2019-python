import click
from typing import List, Tuple, Generator, Set


def read_input(filename: str) -> Tuple[List[str], List[str]]:
    with open(filename) as f:
        wire_a, wire_b = f.read().rstrip('\n').split('\n')
    return wire_a.split(','), wire_b.split(',')


def paths_to_points(paths: List[str]) -> Generator[Tuple[int, int], None, None]:
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


def _manhattan_distance_from_origin(x: int, y: int) -> int:
    return abs(x) + abs(y)


def min_intersection_dist_and_steps(paths_a, paths_b):
    points_a = {point: steps + 1 for steps, point in enumerate(paths_to_points(paths_a))}
    points_b = {point: steps + 1 for steps, point in enumerate(paths_to_points(paths_b))}

    intersections = set(points_a.keys()).intersection(set(points_b.keys()))

    min_distance = min([_manhattan_distance_from_origin(*intersection) for intersection in intersections])
    min_steps = min([points_a[intersection] + points_b[intersection] for intersection in intersections])
    return min_distance, min_steps


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day3.txt', show_default=True,
              help='Path to file containing wire paths (AoC Day3 input.txt)')
def main(input_file):
    wire_a_paths, wire_b_paths = read_input(input_file)

    min_distance, min_steps = min_intersection_dist_and_steps(wire_a_paths, wire_b_paths)
    print(f'Minimum intersection distance: {min_distance}')
    print(f'Minimum intersection steps: {min_steps}')


if __name__ == '__main__':
    main()
