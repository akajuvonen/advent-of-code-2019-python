from abc import ABC, abstractmethod
from typing import List, Optional

import attr


@attr.s(auto_attribs=True)
class IntcodeOperation(ABC):
    intcode: List[int]
    instr_pointer: int
    param_modes: int = attr.ib(init=False)
    halted: bool = attr.ib(init=False, default=False)

    @param_modes.default
    def _parse_instruction(self):
        return self.intcode[self.instr_pointer] // 100

    @abstractmethod
    def execute(self, inputs: List[int]) -> Optional[int]:
        pass

    def _output_to_index(self, value: int):
        """Output value to the position defined by the next intcode step."""
        self.instr_pointer += 1
        output_index = self.intcode[self.instr_pointer]
        self.intcode[output_index] = value

    @property
    def _next_value(self) -> int:
        """Simultaneously parse the next parameter mode (0 or 1), increment pointer and return value"""
        param_mode = self.param_modes % 10
        self.param_modes //= 10
        self.instr_pointer += 1
        return self.intcode[self.instr_pointer] if param_mode else self.intcode[self.intcode[self.instr_pointer]]


class AddOperation(IntcodeOperation):
    """Addition of two values."""
    def execute(self, inputs):
        self._output_to_index(self._next_value + self._next_value)
        self.instr_pointer += 1


class MultiplyOperation(IntcodeOperation):
    """Multiply two values."""
    def execute(self, inputs):
        self._output_to_index(self._next_value * self._next_value)
        self.instr_pointer += 1


class InputOperation(IntcodeOperation):
    """Consume the next input."""
    def execute(self, inputs):
        self._output_to_index(inputs.pop())
        self.instr_pointer += 1


class OutputOperation(IntcodeOperation):
    """Get and return an output value."""
    def execute(self, inputs):
        output = self._next_value
        self.instr_pointer += 1
        return output


class JumpIfTrueOperation(IntcodeOperation):
    """Jump to an index if given value is non-zero."""
    def execute(self, inputs):
        value = self._next_value
        new_pointer = self._next_value
        self.instr_pointer = new_pointer if value else self.instr_pointer + 1


class JumpIfFalseOperation(IntcodeOperation):
    """Jump to an index if given value is zero."""
    def execute(self, inputs):
        value = self._next_value
        new_pointer = self._next_value
        self.instr_pointer = new_pointer if not value else self.instr_pointer + 1


class LessThanOperation(IntcodeOperation):
    """Write 1 to index if the first value < second value."""
    def execute(self, inputs):
        self._output_to_index(1 if self._next_value < self._next_value else 0)
        self.instr_pointer += 1


class EqualsOperation(IntcodeOperation):
    """Write 1 to index if two values are equal."""
    def execute(self, inputs):
        self._output_to_index(1 if self._next_value == self._next_value else 0)
        self.instr_pointer += 1


class HaltOperation(IntcodeOperation):
    """Halt intcode processing."""
    def execute(self, inputs):
        self.halted = True


OPERATIONS = {1: AddOperation,
              2: MultiplyOperation,
              3: InputOperation,
              4: OutputOperation,
              5: JumpIfTrueOperation,
              6: JumpIfFalseOperation,
              7: LessThanOperation,
              8: EqualsOperation,
              99: HaltOperation}


@attr.s(auto_attribs=True)
class IntcodeComputer:
    intcode: List[int]
    inputs: List[int] = attr.ib(init=False, factory=list)
    instr_pointer: int = attr.ib(init=False, default=0)
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
            operation = OPERATIONS[opcode](self.intcode, self.instr_pointer)
            output = operation.execute(self.inputs)
            self.instr_pointer = operation.instr_pointer
            self.halted = operation.halted
            if output is not None:
                self.output = output

    def set_inputs(self, *inputs):
        self.inputs = [i for i in inputs]
        self.inputs.reverse()
