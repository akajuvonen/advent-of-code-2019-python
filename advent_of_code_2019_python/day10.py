from collections import namedtuple
from math import gcd
from typing import Optional, Set, Tuple

import click


Coord = namedtuple('Coord', ['x', 'y'])


def parse_asteroids(filename: str) -> Set[Coord]:
    asteroids = set()
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c == '#':
                    asteroids.add(Coord(x, y))
    return asteroids


def calculate_visible_asteroids(all_asteroids: Set[Coord], location: Coord) -> int:
    unique_line_of_sights = set()
    for asteroid in all_asteroids:
        dx, dy = asteroid.x - location.x, asteroid.y - location.y
        divisor = gcd(dx, dy)
        if divisor:
            unique_line_of_sights.add((dx // divisor, dy // divisor))
    return len(unique_line_of_sights)


def find_best_location(asteroids: Set[Coord]) -> Tuple[Optional[Coord], int]:
    max_visible_asteroids = 0
    best_location = None
    for asteroid in asteroids:
        visible_asteroids = calculate_visible_asteroids(asteroids, asteroid)
        if visible_asteroids > max_visible_asteroids:
            max_visible_asteroids = visible_asteroids
            best_location = asteroid
    return best_location, max_visible_asteroids


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day10.txt', show_default=True,
              help='Path to file containing asteroid locations.')
def main(input_file):
    asteroids = parse_asteroids(input_file)
    best_loc, visible_asteroids = find_best_location(asteroids)
    print(f'Best location at {best_loc} with {visible_asteroids} visible asteroids')


if __name__ == '__main__':
    main()
