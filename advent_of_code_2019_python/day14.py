from typing import Dict

import click


def parse_file(input_file: str) -> Dict[str, Dict[str, int]]:
    reactions = {}
    with open(input_file) as f:
        for line in f:
            line = line.rstrip('\n').replace(' ', '')
            line, result = line.split('=>')
            ingredients = line.split(',')
            recipe = {}
            for ingredient in ingredients:
                name = ingredient.lstrip('0123456789')
                quantity = int(ingredient[:-len(name)])
                recipe[name] = quantity
            reactions[result] = recipe
    return reactions


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day14.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    reactions = parse_file(input_file)
    print(reactions)


if __name__ == '__main__':
    main()
