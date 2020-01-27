from advent_of_code_2019_python.day10 import calculate_visible_asteroids, find_best_location, Coord


ASTEROIDS = {Coord(1, 0), Coord(4, 0), Coord(0, 2), Coord(1, 2), Coord(2, 2), Coord(3, 2), Coord(4, 2), Coord(4, 3),
             Coord(3, 4), Coord(4, 4)}
LOCATION = Coord(3, 4)
SIZE = Coord(5, 5)


def test_calculate_visible_asteroids():
    assert calculate_visible_asteroids(ASTEROIDS, LOCATION, SIZE) == 8


def test_find_best_location():
    location, visible_asteroids = find_best_location(ASTEROIDS, SIZE)
    assert location == Coord(3, 4)
    assert visible_asteroids == 8
