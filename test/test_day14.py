from advent_of_code_2019_python.day14 import calculate_ore


def test_calculate_ingredients():
    reactions = {'FUEL': ({'A': 7, 'E': 1}, 1),
                 'E': ({'A': 7, 'D': 1}, 1),
                 'D': ({'A': 7, 'C': 1}, 1),
                 'C': ({'A': 7, 'B': 1}, 1),
                 'B': ({'ORE': 1}, 1),
                 'A': ({'ORE': 10}, 10)}
    assert calculate_ore(reactions) == 31

    reactions = {'FUEL': ({'AB': 2, 'BC': 3, 'CA': 4}, 1),
                 'CA': ({'C': 4, 'A': 1}, 1),
                 'BC': ({'B': 5, 'C': 7}, 1),
                 'AB': ({'A': 3, 'B': 4}, 1),
                 'C': ({'ORE': 7}, 5),
                 'B': ({'ORE': 8}, 3),
                 'A': ({'ORE': 9}, 2)}
    assert calculate_ore(reactions) == 165
