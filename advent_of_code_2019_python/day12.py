from itertools import permutations
from typing import List

import attr
import click
import numpy as np


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
        self.velocity.x += _get_change(self.position.x, other.position.x)
        self.velocity.y += _get_change(self.position.y, other.position.y)
        self.velocity.z += _get_change(self.position.z, other.position.z)

    def apply_velocity(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

def _get_change(this: int, other: int) -> int:
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


def calculate_total_energy(moons: List[Moon]) -> int:
    total_energy = 0
    for moon in moons:
        potential_energy = abs(moon.position.x) + abs(moon.position.y) + abs(moon.position.z)
        kinetic_energy = abs(moon.velocity.x) + abs(moon.velocity.y) + abs(moon.velocity.z)
        total_energy += potential_energy * kinetic_energy
    return total_energy


def calculate_loop(moons: List[Moon]) -> int:
    xs = np.zeros(len(moons))
    ys = np.zeros(len(moons))
    zs = np.zeros(len(moons))
    for i, moon in enumerate(moons):
        xs[i] = moon.position.x
        ys[i] = moon.position.y
        zs[i] = moon.position.z
    x_steps = _calculate_loop_for_one_axis(xs)
    y_steps = _calculate_loop_for_one_axis(ys)
    z_steps = _calculate_loop_for_one_axis(zs)
    return np.lcm.reduce([x_steps, y_steps, z_steps])


def _calculate_loop_for_one_axis(positions: np.ndarray):
    velocities = np.zeros(len(positions))
    orig_positions = np.copy(positions)
    steps = 0
    while True:
        for this, other in permutations(range(len(positions)), 2):
            velocities[this] += _get_change(positions[this], positions[other])
        for i, v in enumerate(velocities):
            positions[i] += v
        steps += 1
        if np.array_equal(positions, orig_positions) and all(velocities == 0):
            break
    return steps



@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day12.txt', show_default=True,
              help='Path to file containing moon positions.')
def main(input_file):
    moons = parse_input(input_file)
    apply_gravity(moons, 1000)
    print(f'Total energy: {calculate_total_energy(moons)}')

    moons = parse_input(input_file)
    loop_steps = calculate_loop(moons)
    print(f'Steps needed for the system to repeat itself: {loop_steps}')


if __name__ == '__main__':
    main()
