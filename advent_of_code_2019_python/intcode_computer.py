from typing import List, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod

import attr


class Status(Enum):
    RUNNING = auto()
    PAUSED = auto()
    HALTED = auto()


@attr.s(auto_attribs=True)
class IntcodeOperation(ABC):
    intcode: List[int]
    instr_pointer: int
    param_modes: int = attr.ib(init=False)
    halted: bool = attr.ib(init=False, default=False)
    paused: bool = attr.ib(init=False, default=False)

    @param_modes.default
    def _parse_instruction(self):
        return self.intcode[self.instr_pointer] // 100

    @abstractmethod
    def execute(self, input_value: Optional[int]) -> None:
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
    def execute(self, input_value: Optional[int]) -> None:
        self._output_to_index(self._next_value + self._next_value)
        self.instr_pointer += 1


class MultiplyOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> None:
        self._output_to_index(self._next_value * self._next_value)
        self.instr_pointer += 1


class InputOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> None:
        # if input_value is None: status = PAUSED
        # else below
        if input_value is not None:
            self._output_to_index(input_value)
            self.instr_pointer += 1


class OutputOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> int:
        output = self._next_value
        self.instr_pointer += 1
        # self.status = Status.PAUSED
        return output


class JumpIfTrueOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> None:
        value = self._next_value
        new_pointer = self._next_value
        if value:
            self.instr_pointer = new_pointer
        else:
            self.instr_pointer += 1


class JumpIfFalseOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> None:
        value = self._next_value
        new_pointer = self._next_value
        if not value:
            self.instr_pointer = new_pointer
        else:
            self.instr_pointer += 1


class LessThanOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> None:
        self._output_to_index(1 if self._next_value < self._next_value else 0)
        self.instr_pointer += 1


class EqualsOperation(IntcodeOperation):
    def execute(self, input_value: Optional[int]) -> None:
        self._output_to_index(1 if self._next_value == self._next_value else 0)
        self.instr_pointer += 1


@attr.s
class HaltOperation(IntcodeOperation):
    halted: bool = attr.ib(init=False, default=True)

    def execute(self, input_value: Optional[int]) -> None:
        pass


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
    inputs: List[int] = attr.ib(factory=list)
    instr_pointer: int = attr.ib(init=False, default=0)
    output: int = attr.ib(init=False, default=None)
    halted: bool = attr.ib(init=False, default=False)

    def __attrs_post_init__(self):
        self.inputs.reverse()

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            intcode = f.read().rstrip('\n').split(',')
        return cls([int(x) for x in intcode])

    def compute(self):
        """Computes an intcode program result.

        Arguments:
            input_value: An integer given as input to the program.
        """
        while not self.halted:
            input_value = self.next_input
            opcode = self.intcode[self.instr_pointer] % 100
            operation = OPERATIONS[opcode](self.intcode, self.instr_pointer)
            output = operation.execute(input_value)
            self.instr_pointer = operation.instr_pointer
            self.halted = operation.halted
            if output is not None:
                self.output = output
                break
            # remember to set input value to None after it's used

    @property
    def next_input(self):
        return self.inputs.pop() if self.inputs else None
