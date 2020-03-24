from typing import Dict, Tuple

import click


def _parse_name_and_quantity(string: str) -> Tuple[str, int]:
    name = string.lstrip('0123456789')
    quantity = int(string[:-len(name)])
    return name, quantity


def parse_file(input_file: str) -> Dict[str, Dict[str, int]]:
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


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day14.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    reactions = parse_file(input_file)
    print(reactions)


if __name__ == '__main__':
    main()
