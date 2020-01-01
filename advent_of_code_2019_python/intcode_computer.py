from typing import List, Optional

import attr

# Pre-defined opcodes
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
# Take input and save to position
OPCODE_INPUT = 3
# Print output
OPCODE_OUTPUT = 4
# Jump to a specified position if value non-zero
OPCODE_JUMPIFTRUE = 5
# Jump to a specified location if zero
OPCODE_JUMPIFFALSE = 6
# Output 1 to position if first parameter less than second, otherwise 0
OPCODE_LESSTHAN = 7
# Output 1 if parameters equal, otherwise 0
OPCODE_EQUALS = 8
OPCODE_HALT = 99


@attr.s
class IntcodeComputer:
    intcode: List[int] = attr.ib()
    orig_intcode: List[int] = attr.ib(init=False)
    instruction: int = attr.ib(init=False)
    instr_pointer: int = attr.ib(init=False, default=0)
    output: List[int] = attr.ib(factory=list)

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
                if opcode == OPCODE_ADD:
                    self._output_to_index(self._next_value + self._next_value)
                elif opcode == OPCODE_MULTIPLY:
                    self._output_to_index(self._next_value * self._next_value)
                elif opcode == OPCODE_INPUT:
                    self._output_to_index(input_value)
                elif opcode == OPCODE_OUTPUT:
                    self.output.append(self._next_value)
                elif opcode == OPCODE_JUMPIFTRUE:
                    value = self._next_value
                    new_pointer = self._next_value
                    if value:
                        self.instr_pointer = new_pointer
                        continue
                elif opcode == OPCODE_JUMPIFFALSE:
                    value = self._next_value
                    new_pointer = self._next_value
                    if not value:
                        self.instr_pointer = new_pointer
                        continue
                elif opcode == OPCODE_LESSTHAN:
                    self._output_to_index(1 if self._next_value < self._next_value else 0)
                elif opcode == OPCODE_EQUALS:
                    self._output_to_index(1 if self._next_value == self._next_value else 0)
                else:
                    raise ValueError(f'Opcode {opcode} not supported')
                self.instr_pointer += 1
        except IndexError:
            print(f'Intcode index out of range, no instruction {OPCODE_HALT} found, stopping')

    def _output_to_index(self, value: int):
        """Output value to the position defined by the next intcode step."""
        self.instr_pointer += 1
        output_index = self.intcode[self.instr_pointer]
        self.intcode[output_index] = value

    def reset(self):
        """Reset computer to its original state before the program was run"""
        self.intcode = self.orig_intcode.copy()
        self.instr_pointer = 0
        self.output = []

    @property
    def _next_value(self):
        """Simultaneously parse the next parameter mode (0 or 1), increment pointer and return value"""
        param_mode = self.instruction % 10
        self.instruction //= 10
        self.instr_pointer += 1
        return self.intcode[self.instr_pointer] if param_mode else self.intcode[self.intcode[self.instr_pointer]]

    def print_output(self):
        for output in self.output:
            print(output)
