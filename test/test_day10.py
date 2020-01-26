from advent_of_code_2019_python.day10 import calculate_visible_asteroids, find_best_location


def test_calculate_visible_asteroids():
    asteroids = {(1, 0), (4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (3, 4), (4, 4)}
    location = (3, 4)
    size = (5, 5)
    assert calculate_visible_asteroids(asteroids, location, size) == 8


def test_find_best_location():
    asteroids = {(1, 0), (4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (3, 4), (4, 4)}
    size = (5, 5)
    location, visible_asteroids = find_best_location(asteroids, size)
    assert location == (3, 4)
    assert visible_asteroids == 8
