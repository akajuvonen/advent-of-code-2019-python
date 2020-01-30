from advent_of_code_2019_python.day10 import find_best_location, Coord, vaporize_asteroids


def test_find_best_location():
    asteroids = {Coord(1, 0), Coord(4, 0), Coord(0, 2), Coord(1, 2), Coord(2, 2), Coord(3, 2), Coord(4, 2), Coord(4, 3),
                 Coord(3, 4), Coord(4, 4)}
    location, visible_asteroids = find_best_location(asteroids)
    assert location == Coord(3, 4)
    assert visible_asteroids == 8


def test_vaporize_asteroids():
    asteroids = {Coord(3, 2), Coord(3, 3), Coord(3, 1), Coord(4, 3), Coord(2, 4)}
    location = Coord(3, 3)
    vaporized = vaporize_asteroids(asteroids, location)
    assert vaporized == [Coord(3, 2), Coord(4, 3), Coord(2, 4), Coord(3, 1)]
