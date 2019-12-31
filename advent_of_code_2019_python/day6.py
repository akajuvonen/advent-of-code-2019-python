from __future__ import annotations

from collections import defaultdict
from typing import List, DefaultDict

import attr
import click


@attr.s(auto_attribs=True)
class SpaceObject:
    orbiters: List[SpaceObject] = attr.Factory(list)

    def add_orbiter(self, orbiter: SpaceObject):
        self.orbiters.append(orbiter)


def populate_orbits(filename: str) -> DefaultDict[str, SpaceObject]:
    all_objects: DefaultDict = defaultdict(SpaceObject)
    with open(filename) as f:
        for line in f:
            [center_of_mass, orbiter] = line.rstrip('\n').split(')')
            all_objects[center_of_mass].add_orbiter(orbiter)
    print(all_objects)
    return all_objects


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day6.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    populate_orbits(input_file)


if __name__ == '__main__':
    main()
