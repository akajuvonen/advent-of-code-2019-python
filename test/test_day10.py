from advent_of_code_2019_python.day10 import calculate_visible_asteroids


def test_calculate_visible_asteroids():
    asteroids = {(0, 1), (0, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 4), (4, 3), (4, 4)}
    location = (3, 4)
    assert calculate_visible_asteroids(asteroids, location, (5, 5)) == 8
