from collections import namedtuple
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
    velocity: Coord = Coord(x=0, y=0, z=0)

    def update_velocity(self, other_position):
        self.velocity.x = self._get_change(self.position.x, other_position.x)
        self.velocity.y = self._get_change(self.position.y, other_position.y)
        self.velocity.z = self._get_change(self.position.z, other_position.z)

    def apply_velocity(self):
        self.position.x = self.velocity.x
        self.position.y = self.velocity.y
        self.position.z = self.velocity.z

    def _get_change(self, this, other):
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
            moons.append(Moon(position=Coord(x, y, z)))
    return moons


def apply_gravity(moons, steps):
    for _ in range(steps):
        for moon in moons:
            for other in moons:
                moon.update_velocity(other.position)
        for moon in moons:
            moon.apply_velocity()



@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day12.txt', show_default=True,
              help='Path to file containing moon positions.')
def main(input_file):
    moons = parse_input(input_file)
    print(moons)
    moons = apply_gravity(moons, 1)
    print(moons)


if __name__ == '__main__':
    main()
