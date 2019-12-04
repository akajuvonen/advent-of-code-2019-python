from typing import List
import click


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(line.rstrip('\n')) for line in f.readlines()]


def calculate_fuel(weight: int) -> int:
    return weight // 3 - 2


@click.command()
@click.option('--input-file', required=True, type=str,
              help='Path to file containing module weights separated by newlines')
def main(input_file):
    inputs = read_input(input_file)
    total_fuel = sum([calculate_fuel(input) for input in inputs])
    print(f'Total amount of fuel needed: {total_fuel}')


if __name__ == '__main__':
    main()
