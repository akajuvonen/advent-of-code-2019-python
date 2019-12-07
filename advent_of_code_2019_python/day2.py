from typing import List, Optional, Tuple

import click

# Pre-defined opcodes
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT = 99
# How many steps to take to find the next opcode
N_STEPS = 4

EXPECTED_OUTPUT = 19690720


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        intcode = f.read().rstrip('\n').split(',')
    return [int(x) for x in intcode]


def compute(intcode: List[int], noun: Optional[int] = None, verb: Optional[int] = None) -> List[int]:
    new_intcode = intcode.copy()
    # Initialize noun and verb positions (index 1 and 2)
    if noun is not None:
        new_intcode[1] = noun
    if verb is not None:
        new_intcode[2] = verb

    # TODO what if at the end of the list and no 99
    i = 0
    while True:
        opcode = new_intcode[i]
        if opcode == OPCODE_HALT:
            break
        first_index = new_intcode[i+1]
        second_index = new_intcode[i+2]
        output_index = new_intcode[i+3]
        if opcode == OPCODE_ADD:
            new_intcode[output_index] = new_intcode[first_index] + new_intcode[second_index]
        elif opcode == OPCODE_MULTIPLY:
            new_intcode[output_index] = new_intcode[first_index] * new_intcode[second_index]
        else:
            raise ValueError(f'Opcode {opcode} not supported')
        i += 4

    return new_intcode


def find_noun_verb(intcode: List[int], expected_output: int) -> Optional[Tuple[int, int]]:
    max_value = 99
    for noun in range(max_value + 1):
        for verb in range(max_value + 1):
            if compute(intcode, noun, verb)[0] == expected_output:
                return noun, verb
    return None


@click.command()
@click.option('--input-file', required=True, type=str, default='input.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode = read_input(input_file)

    # Return the program to the 1202 program alarm state and get result
    new_intcode = compute(intcode, 12, 2)
    print(new_intcode)

    # Find inputs in positions 1 and 2 that produce the expected output
    noun, verb = find_noun_verb(intcode, EXPECTED_OUTPUT)
    print(f'Pair of inputs that produce output {EXPECTED_OUTPUT}: {noun} and {verb}')


if __name__ == '__main__':
    main()
