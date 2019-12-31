from __future__ import annotations

from typing import Dict, List, Optional

import attr
import click


@attr.s(auto_attribs=True)
class SpaceObject:
    name: str
    parent: Optional[SpaceObject] = None
    orbiters: List[SpaceObject] = attr.Factory(list)

    def add_orbiter(self, orbiter: SpaceObject):
        self.orbiters.append(orbiter)


def populate_orbits(orbit_list: List[str]) -> SpaceObject:
    orbit_dict: Dict[str, List[str]] = {}
    for orbit in orbit_list:
        [center_of_mass, orbiter] = orbit.split(')')
        if center_of_mass not in orbit_dict:
            orbit_dict[center_of_mass] = []
        orbit_dict[center_of_mass].append(orbiter)
    univ_center_of_mass = SpaceObject(name='COM')
    _add_orbiters(univ_center_of_mass, orbit_dict)
    return univ_center_of_mass


def _add_orbiters(space_object: SpaceObject, orbit_dict: Dict[str, list]):
    if space_object.name not in orbit_dict:
        return
    for orbiter_name in orbit_dict[space_object.name]:
        orbiter = SpaceObject(name=orbiter_name)
        space_object.add_orbiter(orbiter)
        _add_orbiters(orbiter, orbit_dict)


def calculate_orbits(univ_center_of_mass: SpaceObject) -> int:
    return _traverse_objects(univ_center_of_mass, 0)


def _traverse_objects(space_object: SpaceObject, count: int) -> int:
    if not space_object.orbiters:
        return count
    total = 0
    for orbiter in space_object.orbiters:
        total += _traverse_objects(orbiter, count+1)
    return total + count


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day6.txt', show_default=True,
              help='Path to file containing space object orbits')
def main(input_file):
    orbit_list = []
    with open(input_file) as f:
        for line in f:
            orbit_list.append(line.rstrip('\n'))
    univ_center_of_mass = populate_orbits(orbit_list)
    orbit_count = calculate_orbits(univ_center_of_mass)
    print(orbit_count)


if __name__ == '__main__':
    main()
