from collections import defaultdict
from typing import Dict, Tuple, DefaultDict

import click
import numpy as np  # type: ignore


def _parse_name_and_quantity(string: str) -> Tuple[str, int]:
    name = string.lstrip('0123456789')
    quantity = int(string[:-len(name)])
    return name, quantity


def parse_file(input_file: str) -> Dict[str, Tuple[Dict[str, int], int]]:
    reactions = {}
    with open(input_file) as f:
        for line in f:
            line = line.rstrip('\n').replace(' ', '')
            line, result = line.split('=>')
            resultname, resultquantity = _parse_name_and_quantity(result)
            ingredients = line.split(',')
            recipe = {}
            for ingredient in ingredients:
                name, quantity = _parse_name_and_quantity(ingredient)
                recipe[name] = quantity
            reactions[resultname] = (recipe, resultquantity)
    return reactions


def calculate_ore(reactions: Dict[str, Tuple[Dict[str, int], int]], fuel_amount: int = 1) -> int:
    """Calculates needed total ore for one unit of FUEL.

    This is done by first calculating needed quantities of basic ingredients
    (ingredients that only need ore) and then calculating total ore after that.
    """
    basic_ingredients: DefaultDict[str, int] = defaultdict(int)
    leftovers: DefaultDict[str, int] = defaultdict(int)
    _calculate_basic_ingredients(reactions, 'FUEL', fuel_amount, basic_ingredients, leftovers)
    needed_ore = 0
    for basic_ingredient in basic_ingredients:
        needed_basic_ingredient = basic_ingredients[basic_ingredient]
        basic_ingredient_produced_per_reaction = reactions[basic_ingredient][1]
        consumed_ore_per_reaction = reactions[basic_ingredient][0]['ORE']
        needed_reactions = int(np.ceil(float(needed_basic_ingredient) / float(basic_ingredient_produced_per_reaction)))
        needed_ore += needed_reactions * consumed_ore_per_reaction
    return needed_ore


def _calculate_basic_ingredients(reactions: Dict[str, Tuple[Dict[str, int], int]], ingredient: str,
                                 needed_quantity: int, basic_ingredients: Dict[str, int], leftovers: Dict[str, int]):
    """Calculates needed basic ingredients while keeping track and using any leftovers from previous reactions."""
    sub_ingredients, produced_quantity = reactions[ingredient]
    if 'ORE' in sub_ingredients:
        basic_ingredients[ingredient] += needed_quantity
        return
    # Consume leftovers
    consumed_leftovers = min(needed_quantity, leftovers[ingredient])
    needed_quantity -= consumed_leftovers
    leftovers[ingredient] -= consumed_leftovers
    # Save any extra to leftovers
    needed_reactions = int(np.ceil(float(needed_quantity) / float(produced_quantity)))
    total_produced_quantity = needed_reactions * produced_quantity
    leftovers[ingredient] += total_produced_quantity - needed_quantity
    for sub_ingredient in sub_ingredients:
        needed_sub_ingredient_per_reaction = sub_ingredients[sub_ingredient]
        needed_sub_ingredient_quantity = needed_reactions * needed_sub_ingredient_per_reaction
        _calculate_basic_ingredients(reactions, sub_ingredient, needed_sub_ingredient_quantity, basic_ingredients,
                                     leftovers)


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day14.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    reactions = parse_file(input_file)
    print(f'Part 1 (needed ore for one FUEL: {calculate_ore(reactions)}')

    # NOTE: The value below obtained by simple (manual) search, do it programmatically
    fuel = 3126714
    print(f'Part 2: FUEL produced with 1 trillion ore: {calculate_ore(reactions, fuel)}')


if __name__ == '__main__':
    main()
