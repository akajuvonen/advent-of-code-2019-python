from itertools import permutations
from typing import List

import attr
import click


@attr.s(auto_attribs=True)
class Coord:
    x: int
    y: int
    z: int


@attr.s(auto_attribs=True)
class Moon:
    position: Coord
    velocity: Coord

    def update_velocity(self, other: 'Moon'):
        self.velocity.x += self._get_change(self.position.x, other.position.x)
        self.velocity.y += self._get_change(self.position.y, other.position.y)
        self.velocity.z += self._get_change(self.position.z, other.position.z)

    def apply_velocity(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def _get_change(self, this: int, other: int) -> int:
        if this == other:
            return 0
        return 1 if this < other else -1


def parse_input(input_file: str) -> List[Moon]:
    moons = []
    with open(input_file) as f:
        for line in f:
            line = line.rstrip('\n').rstrip('>').lstrip('<')
            line = line.replace(' ', '')
            coords = line.split(',')
            x, y, z = tuple(int(c.split('=')[1]) for c in coords)
            moons.append(Moon(position=Coord(x, y, z), velocity=Coord(0, 0, 0)))
    return moons


def apply_gravity(moons: List[Moon], steps: int):
    for _ in range(steps):
        for this, other in permutations(moons, 2):
            this.update_velocity(other)
        for moon in moons:
            moon.apply_velocity()


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day12.txt', show_default=True,
              help='Path to file containing moon positions.')
def main(input_file):
    moons = parse_input(input_file)
    moons = apply_gravity(moons, 1000)


if __name__ == '__main__':
    main()
