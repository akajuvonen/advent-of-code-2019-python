from advent_of_code_2019_python.day12 import apply_gravity, Moon, Coord


def test_velocity():
    moons = [Moon(position=Coord(0, 0, 0), velocity=Coord(0, 0, 0)), Moon(position=Coord(2, 2, 2), velocity=Coord(0, 0, 0))]
    expected = [Moon(Coord(1, 1, 1), Coord(1, 1, 1)), Moon(Coord(1, 1, 1), Coord(-1, -1, -1))]
    apply_gravity(moons, 1)
    assert moons == expected
