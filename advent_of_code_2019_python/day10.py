from math import gcd
from typing import Optional, Set, Tuple

import click


def parse_asteroids(filename: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    asteroids = set()
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c == '#':
                    asteroids.add((x, y))
    return asteroids, (x, y)


def calculate_visible_asteroids(all_asteroids: Set[Tuple[int, int]], location: Tuple[int, int],
                                size: Tuple[int, int]) -> int:
    x, y = location
    max_x, max_y = size
    visible_asteroids = all_asteroids.copy()
    visible_asteroids.remove(location)
    for asteroid in visible_asteroids.copy():
        asteroid_x, asteroid_y = asteroid
        dx, dy = asteroid_x - x, asteroid_y - y
        divisor = gcd(dx, dy)
        dx //= divisor
        dy //= divisor
        current_x, current_y = x + dx, y + dy
        first_asteroid_from_location = True
        while 0 <= current_x < max_x and 0 <= current_y < max_y:
            if (current_x, current_y) in visible_asteroids:
                if first_asteroid_from_location:
                    first_asteroid_from_location = False
                else:
                    visible_asteroids.remove((current_x, current_y))
            current_x += dx
            current_y += dy
    return len(visible_asteroids)


def find_best_location(asteroids: Set[Tuple[int, int]], size: Tuple[int, int]) \
        -> Tuple[Optional[Tuple[int, int]], int]:
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
    asteroids, size = parse_asteroids(input_file)
    best_loc, visible_asteroids = find_best_location(asteroids, size)
    print(f'Best location at {best_loc} with {visible_asteroids} visible asteroids')


if __name__ == '__main__':
    main()
