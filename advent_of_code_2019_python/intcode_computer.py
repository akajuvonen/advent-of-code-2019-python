from abc import ABC, abstractmethod
from typing import List, Optional, DefaultDict
from collections import defaultdict

import attr


def _list_to_defaultdict(l: List[int]) -> DefaultDict[int, int]:
    d: DefaultDict[int, int] = defaultdict(int)
    for i, x in enumerate(l):
        d[i] = x
    return d


@attr.s(auto_attribs=True)
class IntcodeOperation(ABC):
    intcode: DefaultDict[int, int]
    instr_pointer: int
    inputs: List[int]
    relative_base: int
    param_modes: int = attr.ib(init=False)
    halted: bool = attr.ib(init=False, default=False)

    @param_modes.default
    def _parse_instruction(self):
        return self.intcode[self.instr_pointer] // 100

    @abstractmethod
    def execute(self) -> Optional[int]:
        pass

    def _output_to_index(self, value: int):
        """Output value to the position defined by the next intcode step."""
        self.instr_pointer += 1
        output_index = self.intcode[self.instr_pointer]
        self.intcode[output_index] = value

    @property
    def _next_value(self) -> int:
        """Simultaneously parse the next parameter mode (0, 1 or 2), increment pointer and return value"""
        param_mode = self.param_modes % 10
        self.param_modes //= 10
        self.instr_pointer += 1
        # If immediate mode, return the actual value
        if param_mode == 1:
            return self.intcode[self.instr_pointer]
        # In position mode the value is retrieved from given address
        address = self.intcode[self.instr_pointer]
        # In relative mode the address is adjusted by relative base
        if param_mode == 2:
            address += self.relative_base
        return self.intcode[address]


class AddOperation(IntcodeOperation):
    """Addition of two values."""
    def execute(self):
        self._output_to_index(self._next_value + self._next_value)
        self.instr_pointer += 1


class MultiplyOperation(IntcodeOperation):
    """Multiply two values."""
    def execute(self):
        self._output_to_index(self._next_value * self._next_value)
        self.instr_pointer += 1


class InputOperation(IntcodeOperation):
    """Consume the next input."""
    def execute(self):
        self._output_to_index(self.inputs.pop())
        self.instr_pointer += 1


class OutputOperation(IntcodeOperation):
    """Get and return an output value."""
    def execute(self):
        output = self._next_value
        self.instr_pointer += 1
        return output


class JumpIfTrueOperation(IntcodeOperation):
    """Jump to an index if given value is non-zero."""
    def execute(self):
        value = self._next_value
        new_pointer = self._next_value
        self.instr_pointer = new_pointer if value else self.instr_pointer + 1


class JumpIfFalseOperation(IntcodeOperation):
    """Jump to an index if given value is zero."""
    def execute(self):
        value = self._next_value
        new_pointer = self._next_value
        self.instr_pointer = new_pointer if not value else self.instr_pointer + 1


class LessThanOperation(IntcodeOperation):
    """Write 1 to index if the first value < second value."""
    def execute(self):
        self._output_to_index(1 if self._next_value < self._next_value else 0)
        self.instr_pointer += 1


class EqualsOperation(IntcodeOperation):
    """Write 1 to index if two values are equal."""
    def execute(self):
        self._output_to_index(1 if self._next_value == self._next_value else 0)
        self.instr_pointer += 1


class HaltOperation(IntcodeOperation):
    """Halt intcode processing."""
    def execute(self):
        self.halted = True


class AdjustRelativeBaseOperation(IntcodeOperation):
    """Adjust the relative base value."""
    def execute(self):
        self.relative_base += self._next_value
        self.instr_pointer += 1


OPERATIONS = {1: AddOperation,
              2: MultiplyOperation,
              3: InputOperation,
              4: OutputOperation,
              5: JumpIfTrueOperation,
              6: JumpIfFalseOperation,
              7: LessThanOperation,
              8: EqualsOperation,
              9: AdjustRelativeBaseOperation,
              99: HaltOperation}


@attr.s
class IntcodeComputer:
    intcode: DefaultDict[int, int] = attr.ib(converter=_list_to_defaultdict)
    inputs: List[int] = attr.ib(init=False, factory=list)
    instr_pointer: int = attr.ib(init=False, default=0)
    relative_base: int = attr.ib(init=False, default=0)
    output: int = attr.ib(init=False, default=None)
    halted: bool = attr.ib(init=False, default=False)

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            intcode = f.read().rstrip('\n').split(',')
        return cls([int(x) for x in intcode])

    def compute(self):
        """Computes an intcode program result.

        First, the opcode is parsed and correct operation is selected based on that.
        A pointer to available inputs is provided to the operation, which it may optionally consume.
        The operation return an output value or None. If an output is returned, processing is paused.
        Instruction pointer and halt status are updated.
        """
        output = None
        while not self.halted and output is None:
            opcode = self.intcode[self.instr_pointer] % 100
            operation = OPERATIONS[opcode](self.intcode, self.instr_pointer, self.inputs, self.relative_base)
            output = operation.execute()
            self.instr_pointer = operation.instr_pointer
            self.relative_base = operation.relative_base
            self.halted = operation.halted
            if output is not None:
                self.output = output

    def set_inputs(self, *inputs):
        self.inputs = [i for i in inputs]
        self.inputs.reverse()

    @property
    def intcode_aslist(self):
        return [x for x in self.intcode.values()]
