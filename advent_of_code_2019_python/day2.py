from typing import Optional, Tuple

import click

from advent_of_code_2019_python import IntcodeComputer

EXPECTED_OUTPUT = 19690720


def find_noun_verb(intcode_computer: IntcodeComputer, expected_output: int) -> Optional[Tuple[int, int]]:
    """Finds integers at intcode indices 1 and 2 that produce the expected output
    on a given intcode program.

    Arguments:
        intcode_computer: Intcode computer loaded with the desired intcode program.
        expected_output: The expected output integer that should be stored at index 0
            after executing the program.

    Returns:
        Integers for positions 1 and 2 that produce the expected output.
    """
    max_value = 99
    for noun in range(max_value + 1):
        for verb in range(max_value + 1):
            intcode_computer.reset()
            intcode_computer.intcode[1] = noun
            intcode_computer.intcode[2] = verb
            intcode_computer.compute()
            if intcode_computer.intcode[0] == expected_output:
                return intcode_computer.intcode[1], intcode_computer.intcode[2]
    return None


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day2.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)

    # Return the program to the 1202 program alarm state and get result
    intcode_computer.intcode[1] = 12
    intcode_computer.intcode[2] = 2
    intcode_computer.compute()
    print(f'Program output at index 0: {intcode_computer.intcode[0]}')

    # Find inputs in positions 1 and 2 that produce the expected output
    noun, verb = find_noun_verb(intcode_computer, EXPECTED_OUTPUT)
    print(f'Pair of inputs that produce output {EXPECTED_OUTPUT}: {noun} and {verb}')


if __name__ == '__main__':
    main()
