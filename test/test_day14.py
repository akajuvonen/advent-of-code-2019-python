from advent_of_code_2019_python.day14 import calculate_ore


def test_calculate_ingredients():
    reactions = {'FUEL': ({'A': 7, 'E': 1}, 1),
                 'E': ({'A': 7, 'D': 1}, 1),
                 'D': ({'A': 7, 'C': 1}, 1),
                 'C': ({'A': 7, 'B': 1}, 1),
                 'B': ({'ORE': 1}, 1),
                 'A': ({'ORE': 10}, 10)}
    needed_ore = calculate_ore(reactions)
    assert needed_ore == 31
