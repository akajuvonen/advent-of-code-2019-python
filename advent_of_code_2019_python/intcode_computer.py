from typing import List, Optional

import attr

# Pre-defined opcodes
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_HALT = 99


@attr.s
class IntcodeComputer:
    intcode: List[int] = attr.ib()
    orig_intcode = attr.ib(init=False)

    @orig_intcode.default
    def _init_orig_intcode(self):
        return self.intcode.copy()

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            intcode = f.read().rstrip('\n').split(',')
        return cls([int(x) for x in intcode])

    def compute_intcode(self, noun: Optional[int] = None, verb: Optional[int] = None,
                        input_value: int = 1):
        """Computes an intcode program result.

        Arguments:
            intcode: List of integers containing opcodes, two input positions and
                output positions to save the result to.
            noun: An integer at index 1, known as noun. Affects the final results.
            verb: An integer at index 2, known as verb.
            input_value: An integer given as input to the program.
        """
        # Initialize noun and verb positions (index 1 and 2)
        if noun is not None:
            self.intcode[1] = noun
        if verb is not None:
            self.intcode[2] = verb

        try:
            i = 0
            while True:
                # The last two digits of the instruction
                instruction = self.intcode[i]
                opcode = instruction % 100
                instruction //= 100
                if opcode == OPCODE_HALT:
                    break
                n_steps = 4
                if opcode == OPCODE_ADD:
                    first_param_mode, instruction = _pop_last_digit(instruction)
                    second_param_mode, instruction = _pop_last_digit(instruction)
                    first_value = self.intcode[i+1] if first_param_mode else self.intcode[self.intcode[i+1]]
                    second_value = self.intcode[i+2] if second_param_mode else self.intcode[self.intcode[i+2]]
                    output_index = self.intcode[i+3]
                    self.intcode[output_index] = first_value + second_value
                elif opcode == OPCODE_MULTIPLY:
                    first_param_mode, instruction = _pop_last_digit(instruction)
                    second_param_mode, instruction = _pop_last_digit(instruction)
                    first_value = self.intcode[i+1] if first_param_mode else self.intcode[self.intcode[i+1]]
                    second_value = self.intcode[i+2] if second_param_mode else self.intcode[self.intcode[i+2]]
                    output_index = self.intcode[i+3]
                    self.intcode[output_index] = first_value * second_value
                elif opcode == OPCODE_INPUT:
                    self.intcode[self.intcode[i+1]] = input_value
                    n_steps = 2
                elif opcode == OPCODE_OUTPUT:
                    param_mode, instruction = _pop_last_digit(instruction)
                    output_value = self.intcode[i+1] if param_mode else self.intcode[self.intcode[i+1]]
                    print(output_value)
                    n_steps = 2
                else:
                    raise ValueError(f'Opcode {opcode} not supported')
                i += n_steps
        except IndexError:
            print(f'Intcode index out of range, no instruction {OPCODE_HALT} found, stopping')

    def reset(self):
        self.intcode = self.orig_intcode.copy()

    @property
    def output(self):
        return self.intcode[0]


def _pop_last_digit(instruction):
    digit = instruction % 10
    instruction //= 10
    return digit, instruction
