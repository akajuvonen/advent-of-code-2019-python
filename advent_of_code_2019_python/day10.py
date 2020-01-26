import click
from typing import Set, Tuple


def parse_asteroids(filename: str) -> Tuple[Set[Tuple[int, int]], int, int]:
    asteroids = set()
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c == '#':
                    asteroids.add((x, y))
    return asteroids, x, y


def calculate_visible_asteroids(all_asteroids: Set[Tuple[int, int]], location: Tuple[int, int],
                                size: Tuple[int, int]) -> int:
    visible_asteroids = all_asteroids.copy()
    visible_asteroids.remove(location)
    for asteroid in visible_asteroids.copy():
        gcd = _gcd(*asteroid)
        first = True
        location = tuple([coord // gcd for coord in asteroid])
        while all([b < a for a, b in zip(size, location)]):
            if location in visible_asteroids:
                if first:
                    first = False
                else:
                    visible_asteroids.remove(location)
            location = tuple([coord + gcd for coord in location])
    return len(visible_asteroids)


def _gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day10.txt', show_default=True,
              help='Path to file containing asteroid locations.')
def main(input_file):
    asteroids, size = parse_asteroids(input_file)


if __name__ == '__main__':
    main()
