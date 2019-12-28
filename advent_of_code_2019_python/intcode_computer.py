from typing import List, Optional

# Pre-defined opcodes
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT = 99
# How many steps to take to find the next opcode
N_STEPS = 4


class IntcodeComputer:

    @staticmethod
    def compute(intcode: List[int], noun: Optional[int] = None, verb: Optional[int] = None, input: int = 1) \
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
            input: An integer given as input to the program.

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
                i += N_STEPS
        except IndexError:
            print(f'Intcode index out of range, no instruction {OPCODE_HALT} found, stopping')

        return new_intcode
