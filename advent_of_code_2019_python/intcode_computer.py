from typing import List, Optional

# Pre-defined opcodes
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_HALT = 99


def compute_intcode(intcode: List[int], noun: Optional[int] = None, verb: Optional[int] = None, input_value: int = 1) \
        -> List[int]:
    """Computes  an intcode program result.
    The intcode program contains an opcode (1, 2, or 99 for add, multiply, halt respectively)
    and two input indices. The results after performing specified operation is saved to
    output index. The next opcode is always 4 steps after the previous one.
    Check https://adventofcode.com/2019/day/2 for details on what it's supposed to do.

    Arguments:
        intcode: List of integers containing opcodes, two input positions and
            output positions to save the result to.
        noun: An integer at index 1, known as noun. Affects the final results.
        verb: An integer at index 2, known as verb.
        input_value: An integer given as input to the program.

    Returns:
        Final intcode program after performing all the operations.
    """
    new_intcode = intcode.copy()
    # Initialize noun and verb positions (index 1 and 2)
    if noun is not None:
        new_intcode[1] = noun
    if verb is not None:
        new_intcode[2] = verb

    try:
        i = 0
        while True:
            # The last two digits of the instruction
            instruction = new_intcode[i]
            opcode = instruction % 100
            instruction //= 100
            if opcode == OPCODE_HALT:
                break
            n_steps = 4
            if opcode == OPCODE_ADD:
                first_param_mode, instruction = _pop_last_digit(instruction)
                second_param_mode, instruction = _pop_last_digit(instruction)
                first_value = new_intcode[i+1] if first_param_mode else new_intcode[new_intcode[i+1]]
                second_value = new_intcode[i+2] if second_param_mode else new_intcode[new_intcode[i+2]]
                output_index = new_intcode[i+3]
                new_intcode[output_index] = first_value + second_value
            elif opcode == OPCODE_MULTIPLY:
                first_param_mode, instruction = _pop_last_digit(instruction)
                second_param_mode, instruction = _pop_last_digit(instruction)
                first_value = new_intcode[i+1] if first_param_mode else new_intcode[new_intcode[i+1]]
                second_value = new_intcode[i+2] if second_param_mode else new_intcode[new_intcode[i+2]]
                output_index = new_intcode[i+3]
                new_intcode[output_index] = first_value * second_value
            elif opcode == OPCODE_INPUT:
                new_intcode[new_intcode[i+1]] = input_value
                n_steps = 2
            elif opcode == OPCODE_OUTPUT:
                param_mode, instruction = _pop_last_digit(instruction)
                output_value = new_intcode[i+1] if param_mode else new_intcode[new_intcode[i+1]]
                print(output_value)
                n_steps = 2
            else:
                raise ValueError(f'Opcode {opcode} not supported')
            i += n_steps
    except IndexError:
        print(f'Intcode index out of range, no instruction {OPCODE_HALT} found, stopping')

    return new_intcode


def _pop_last_digit(instruction):
    digit = instruction % 10
    instruction //= 10
    return digit, instruction
