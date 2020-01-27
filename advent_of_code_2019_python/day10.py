from collections import namedtuple
from math import gcd
from typing import Optional, Set, Tuple

import click


Coord = namedtuple('Coord', ['x', 'y'])


def parse_asteroids_with_max_size(filename: str) -> Tuple[Set[Coord], Coord]:
    asteroids = set()
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c == '#':
                    asteroids.add(Coord(x, y))
    return asteroids, Coord(x, y)


def calculate_visible_asteroids(all_asteroids: Set[Coord], location: Coord, size: Coord) -> int:
    visible_asteroids = all_asteroids.copy()
    visible_asteroids.remove(location)
    for asteroid in visible_asteroids.copy():
        dx, dy = asteroid.x - location.x, asteroid.y - location.y
        divisor = gcd(dx, dy)
        dx //= divisor
        dy //= divisor
        current_loc = Coord(location.x + dx, location.y + dy)
        first_asteroid_from_location = True
        while 0 <= current_loc.x < size.x and 0 <= current_loc.y < size.y:
            if current_loc in visible_asteroids:
                if first_asteroid_from_location:
                    first_asteroid_from_location = False
                else:
                    visible_asteroids.remove(current_loc)
            current_loc = Coord(current_loc.x + dx, current_loc.y + dy)
    return len(visible_asteroids)


def find_best_location(asteroids: Set[Coord], size: Coord) -> Tuple[Optional[Coord], int]:
    max_visible_asteroids = 0
    best_location = None
    for asteroid in asteroids:
        visible_asteroids = calculate_visible_asteroids(asteroids, asteroid, size)
        if visible_asteroids > max_visible_asteroids:
            max_visible_asteroids = visible_asteroids
            best_location = asteroid
    return best_location, max_visible_asteroids


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day10.txt', show_default=True,
              help='Path to file containing asteroid locations.')
def main(input_file):
    asteroids, size = parse_asteroids_with_max_size(input_file)
    best_loc, visible_asteroids = find_best_location(asteroids, size)
    print(f'Best location at {best_loc} with {visible_asteroids} visible asteroids')


if __name__ == '__main__':
    main()
