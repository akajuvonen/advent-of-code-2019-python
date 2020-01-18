from typing import List, Optional
from enum import Enum, auto

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


class Status(Enum):
    RUNNING = auto()
    PAUSED = auto()
    HALTED = auto()


@attr.s
class IntcodeComputer:
    intcode: List[int] = attr.ib()
    orig_intcode: List[int] = attr.ib(init=False)
    instruction: int = attr.ib(init=False)
    instr_pointer: int = attr.ib(init=False, default=0)
    output: int = attr.ib(init=False, default=None)
    status: Status = attr.ib(init=False, default=Status.RUNNING)

    @orig_intcode.default
    def _init_orig_intcode(self):
        return self.intcode.copy()

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            intcode = f.read().rstrip('\n').split(',')
        return cls([int(x) for x in intcode])

    def compute(self, input_value: Optional[int] = None):
        """Computes an intcode program result.

        Arguments:
            input_value: An integer given as input to the program.
        """
        self.status = Status.RUNNING
        while self.status is Status.RUNNING:
            # The last two digits of the instruction
            self.instruction = self.intcode[self.instr_pointer]
            opcode = self.instruction % 100
            self.instruction //= 100
            if opcode == OPCODE_HALT:
                self.status = Status.HALTED
            elif opcode == OPCODE_ADD:
                self._output_to_index(self._next_value + self._next_value)
                self.instr_pointer += 1
            elif opcode == OPCODE_MULTIPLY:
                self._output_to_index(self._next_value * self._next_value)
                self.instr_pointer += 1
            elif opcode == OPCODE_INPUT:
                if input_value is None:
                    self.status = Status.PAUSED
                else:
                    self._output_to_index(input_value)
                    input_value = None
                    self.instr_pointer += 1
            elif opcode == OPCODE_OUTPUT:
                self.output = self._next_value
                self.instr_pointer += 1
                self.status = Status.PAUSED
            elif opcode == OPCODE_JUMPIFTRUE:
                value = self._next_value
                new_pointer = self._next_value
                if value:
                    self.instr_pointer = new_pointer
                else:
                    self.instr_pointer += 1
            elif opcode == OPCODE_JUMPIFFALSE:
                value = self._next_value
                new_pointer = self._next_value
                if not value:
                    self.instr_pointer = new_pointer
                else:
                    self.instr_pointer += 1
            elif opcode == OPCODE_LESSTHAN:
                self._output_to_index(1 if self._next_value < self._next_value else 0)
                self.instr_pointer += 1
            elif opcode == OPCODE_EQUALS:
                self._output_to_index(1 if self._next_value == self._next_value else 0)
                self.instr_pointer += 1

    @property
    def halted(self):
        return self.status is Status.HALTED

    def _output_to_index(self, value: int):
        """Output value to the position defined by the next intcode step."""
        self.instr_pointer += 1
        output_index = self.intcode[self.instr_pointer]
        self.intcode[output_index] = value

    def reset(self):
        """Reset computer to its original state before the program was run"""
        self.intcode = self.orig_intcode.copy()
        self.instr_pointer = 0

    @property
    def _next_value(self):
        """Simultaneously parse the next parameter mode (0 or 1), increment pointer and return value"""
        param_mode = self.instruction % 10
        self.instruction //= 10
        self.instr_pointer += 1
        return self.intcode[self.instr_pointer] if param_mode else self.intcode[self.intcode[self.instr_pointer]]
