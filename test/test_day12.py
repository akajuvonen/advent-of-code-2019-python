from advent_of_code_2019_python.day12 import apply_gravity, Moon, Coord


def test_velocity():
    moons = [Moon(Coord(0, 0, 0), velocity=Coord(0, 0, 0)), Moon(Coord(2, 2, 2), Coord(0, 0, 0))]
    apply_gravity(moons, 1)
    assert moons[0].position.x == 1
    assert moons[0].velocity.x == 1
    assert moons[1].position.x == 1
    assert moons[1].velocity.x == -1
