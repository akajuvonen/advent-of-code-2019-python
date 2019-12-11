import pytest
from advent_of_code_2019_python.day3 import calculate_path, intersection_distances, intersection_steps


@pytest.mark.parametrize('paths_a, paths_b, expected_distance',
                         [(['R8', 'U5', 'L5', 'D3'], ['U7', 'R6', 'D4', 'L4'], 6),
                          (['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
                           ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'], 159),
                          (['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
                           ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'], 135)])
def test_minimum_distance(paths_a, paths_b, expected_distance):
    points_a = [path for path in calculate_path(paths_a)]
    points_b = [path for path in calculate_path(paths_b)]
    distance, _ = intersection_distances(points_a, points_b)
    assert min(distance) == expected_distance


@pytest.mark.parametrize('paths_a, paths_b, expected_steps',
                         [(['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
                           ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'], 610),
                          (['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
                           ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'], 410)])
def test_minimum_steps(paths_a, paths_b, expected_steps):
    points_a = [path for path in calculate_path(paths_a)]
    points_b = [path for path in calculate_path(paths_b)]
    _, intersections = intersection_distances(points_a, points_b)
    steps = intersection_steps(points_a, points_b, intersections)
    assert min(steps) == expected_steps
