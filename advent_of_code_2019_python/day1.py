from typing import List
import click


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(line.rstrip('\n')) for line in f.readlines()]


def calculate_fuel(mass: int) -> int:
    """Calculates the amount of fuel needed for a module with mass `mass`.
    Fuel needed for the mass of the fuel itself is not taken into account.

    Arguments:
        mass: Mass of the module to calculate needed fuel for.

    Returns:
        Amount of fuel needed for given mass excluding the fuel itself..
    """
    return max(mass // 3 - 2, 0)


def calculate_total_fuel(mass: int) -> int:
    """Calculates total amount of fuel needed for a module with mass
    `mass` including the mass of the fuel itself. Amounts rounding to 0
    or negative are considered 0.

    Arguments:
        mass: Mass of the module to calculate needed fuel for.

    Returns:
        Total amount of fuel needed including the fuel itself.
    """
    total_fuel = 0
    remaining_mass = mass
    while True:
        remaining_mass = calculate_fuel(remaining_mass)
        assert remaining_mass >= 0
        if remaining_mass == 0:
            return total_fuel
        total_fuel += remaining_mass


@click.command()
@click.option('--input-file', required=True, type=str,
              help='Path to file containing module weights separated by newlines')
def main(input_file):
    masses = read_input(input_file)

    initial_fuel = sum([calculate_fuel(mass) for mass in masses])
    print(f'Amount of fuel needed for modules: {initial_fuel}')

    total_fuel = sum([calculate_total_fuel(mass)for mass in masses])
    print(f'Amount of fuel needed for modules and fuel: {total_fuel}')


if __name__ == '__main__':
    main()
