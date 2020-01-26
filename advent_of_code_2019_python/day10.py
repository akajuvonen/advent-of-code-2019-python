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


def calculate_visible_asteroids(all_asteroids: Set[Tuple[int, ...]], location: Tuple[int, ...],
                                size: Tuple[int, ...]) -> int:
    # Copy to avoid changing the original set
    visible_asteroids = all_asteroids.copy()
    visible_asteroids.remove(location)
    # Iterate over a copy and modify the original
    for asteroid in visible_asteroids.copy():
        diff = tuple([b - a for a, b in zip(location, asteroid)])
        gcd = _gcd(*diff)
        diff = tuple([x // gcd for x in diff])
        step = tuple([a + b for a, b in zip(location, diff)])
        first = True
        # While not going outside the asteroid field
        while all([0 <= b < a for a, b in zip(size, step)]):
            if step in visible_asteroids:
                if first:
                    # Never remove the first asteroid on line of sight
                    first = False
                else:
                    # Remove any asteroid blocked by the first one
                    visible_asteroids.remove(step)
            step = tuple([a + b for a, b in zip(step, diff)])
    return len(visible_asteroids)


def _gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return abs(a)


def find_best_location(asteroids: Set[Tuple[int, ...]], size: Tuple[int, ...]) \
        -> Tuple[Optional[Tuple[int, ...]], int]:
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
