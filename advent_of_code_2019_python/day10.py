from collections import namedtuple
from math import atan2, degrees, gcd
from typing import List, Optional, Set, Tuple

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


def _calculate_unique_lines_of_sight(asteroids: Set[Coord], location: Coord) -> Set[Coord]:
    """Calculates unique lines of sight, which means lines which directly lead to one or more asteroids."""
    unique_line_of_sights = set()
    for asteroid in asteroids:
        dx, dy = asteroid.x - location.x, asteroid.y - location.y
        divisor = gcd(dx, dy)
        if divisor:
            unique_line_of_sights.add(Coord(dx // divisor, dy // divisor))
    return unique_line_of_sights


def find_best_location(asteroids: Set[Coord]) -> Tuple[Optional[Coord], int]:
    """Find location with maximum visible asteroids."""
    max_visible_asteroids = 0
    best_location = None
    for asteroid in asteroids:
        visible_asteroids = len(_calculate_unique_lines_of_sight(asteroids, asteroid))
        if visible_asteroids > max_visible_asteroids:
            max_visible_asteroids = visible_asteroids
            best_location = asteroid
    return best_location, max_visible_asteroids


def vaporize_asteroids(asteroids: Set[Coord], location: Coord) -> List[Coord]:
    """Vaporize asteroids with a lazer turning 360 degrees multiple times. Visible asteroids will be destroyed
    each rotation.
    """
    vaporized = []
    remaining_asteroids = asteroids.copy()
    remaining_asteroids.remove(location)
    while remaining_asteroids:
        loss = _calculate_unique_lines_of_sight(remaining_asteroids, location)
        loss_sorted = sorted(loss, key=lambda coord: degrees(atan2(coord.x, -coord.y)) % 360)
        for los in loss_sorted:
            pos = location
            while pos := Coord(pos.x + los.x, pos.y + los.y):
                if pos in remaining_asteroids:
                    remaining_asteroids.remove(pos)
                    vaporized.append(pos)
                    break
    return vaporized


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day10.txt', show_default=True,
              help='Path to file containing asteroid locations.')
def main(input_file):
    asteroids = parse_asteroids(input_file)
    best_loc, visible_asteroids = find_best_location(asteroids)
    print(f'Best location at {best_loc} with {visible_asteroids} visible asteroids')

    vaporized = vaporize_asteroids(asteroids, best_loc)
    print(vaporized[199])


if __name__ == '__main__':
    main()
