from typing import List, Optional, Tuple
from advent_of_code_2019_python import intcode_computer

import click

EXPECTED_OUTPUT = 19690720


def find_noun_verb(intcode: List[int], expected_output: int) -> Optional[Tuple[int, int]]:
    """Finds integers at intcode indices 1 and 2 that produce the expected output
    on a given intcode program.

    Arguments:
        intcode: Intcode program as a list.
        expected_output: The expected output integer that should be stored at index 0
            after executing the program.

    Returns:
        Integers for positions 1 and 2 that produce the expected output.
    """
    max_value = 99
    for noun in range(max_value + 1):
        for verb in range(max_value + 1):
            if intcode_computer.compute_intcode(intcode, noun, verb)[0] == expected_output:
                return noun, verb
    return None


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day2.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode = intcode_computer.read_input(input_file)

    # Return the program to the 1202 program alarm state and get result
    new_intcode = intcode_computer.compute_intcode(intcode, 12, 2)
    print(new_intcode)
    print(f'Program output at index 0: {new_intcode[0]}')

    # Find inputs in positions 1 and 2 that produce the expected output
    noun, verb = find_noun_verb(intcode, EXPECTED_OUTPUT)
    print(f'Pair of inputs that produce output {EXPECTED_OUTPUT}: {noun} and {verb}')


if __name__ == '__main__':
    main()
