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
    orig_intcode: List[int] = attr.ib(init=False)
    instruction: int = attr.ib(init=False)
    instr_pointer: int = attr.ib(init=False, default=0)

    @orig_intcode.default
    def _init_orig_intcode(self):
        return self.intcode.copy()

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            intcode = f.read().rstrip('\n').split(',')
        return cls([int(x) for x in intcode])

    def compute(self, noun: Optional[int] = None, verb: Optional[int] = None, input_value: int = 1):
        """Computes an intcode program result.

        Arguments:
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
            while True:
                # The last two digits of the instruction
                self.instruction = self.intcode[self.instr_pointer]
                opcode = self.instruction % 100
                self.instruction //= 100
                if opcode == OPCODE_HALT:
                    break
                n_steps = 4
                if opcode == OPCODE_ADD:
                    self._add_or_multiply()
                elif opcode == OPCODE_MULTIPLY:
                    self._add_or_multiply(multiply=True)
                elif opcode == OPCODE_INPUT:
                    self.intcode[self.intcode[self.instr_pointer+1]] = input_value
                    n_steps = 2
                elif opcode == OPCODE_OUTPUT:
                    param_mode = self._pop_last_digit()
                    output_value = self.intcode[self.instr_pointer+1] if param_mode else self.intcode[self.intcode[
                        self.instr_pointer+1]]
                    print(output_value)
                    n_steps = 2
                else:
                    raise ValueError(f'Opcode {opcode} not supported')
                self.instr_pointer += n_steps
        except IndexError:
            print(f'Intcode index out of range, no instruction {OPCODE_HALT} found, stopping')

    def _add_or_multiply(self, multiply=False):
        first_param_mode = self._pop_last_digit()
        second_param_mode = self._pop_last_digit()
        first_value = self.intcode[self.instr_pointer + 1] if first_param_mode else self.intcode[
            self.intcode[self.instr_pointer + 1]]
        second_value = self.intcode[self.instr_pointer + 2] if second_param_mode else self.intcode[
            self.intcode[self.instr_pointer + 2]]
        output_index = self.intcode[self.instr_pointer + 3]
        if multiply:
            self.intcode[output_index] = first_value * second_value
        else:
            self.intcode[output_index] = first_value + second_value

    def reset(self):
        self.intcode = self.orig_intcode.copy()
        self.instr_pointer = 0

    @property
    def output(self):
        return self.intcode[0]

    def _pop_last_digit(self):
        digit = self.instruction % 10
        self.instruction //= 10
        return digit
