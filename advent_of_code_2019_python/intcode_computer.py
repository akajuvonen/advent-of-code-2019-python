from abc import ABC, abstractmethod
from collections import defaultdict
from typing import DefaultDict, List, Optional

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

    def output_to_index(self, value: int):
        """Output value to the position defined by the next intcode step.
        The output address might also be relative.

        Arguments:
            value: The value that will be output to specific address.
        """
        self.intcode[self._get_address()] = value

    def get_next_value(self) -> int:
        """Simultaneously parse the next parameter mode (0, 1 or 2), increment pointer and return value.

        Returns:
            The value in intcode position, or the value in address given by this position.
        """
        return self.intcode[self._get_address()]

    def _get_address(self):
        """Get address of the next value. It may be the direct value, or the value in address indicated
        by the value. The address may also be adjusted by relative base value.
        """
        param_mode = self._get_next_parameter_mode()
        # Immediate mode, parameter mode is the value itself
        if param_mode == 1:
            address = self.instr_pointer
        else:
            # In position mode the value is retrieved from given address
            address = self.intcode[self.instr_pointer]
            # If relative mode, the address is adjusted with relative base
            if param_mode == 2:
                address += self.relative_base
        return address

    def _get_next_parameter_mode(self):
        """Parse the next parameter mode."""
        param_mode = self.param_modes % 10
        self.param_modes //= 10
        self.instr_pointer += 1
        return param_mode


class AddOperation(IntcodeOperation):
    """Addition of two values."""
    def execute(self):
        self.output_to_index(self.get_next_value() + self.get_next_value())
        self.instr_pointer += 1


class MultiplyOperation(IntcodeOperation):
    """Multiply two values."""
    def execute(self):
        self.output_to_index(self.get_next_value() * self.get_next_value())
        self.instr_pointer += 1


class InputOperation(IntcodeOperation):
    """Consume the next input. Inputs can be anything that support pop()."""
    def execute(self):
        self.output_to_index(self.inputs.pop())
        self.instr_pointer += 1


class OutputOperation(IntcodeOperation):
    """Get and return an output value."""
    def execute(self):
        output = self.get_next_value()
        self.instr_pointer += 1
        return output


class JumpIfTrueOperation(IntcodeOperation):
    """Jump to an index if given value is non-zero."""
    def execute(self):
        value = self.get_next_value()
        new_pointer = self.get_next_value()
        self.instr_pointer = new_pointer if value else self.instr_pointer + 1


class JumpIfFalseOperation(IntcodeOperation):
    """Jump to an index if given value is zero."""
    def execute(self):
        value = self.get_next_value()
        new_pointer = self.get_next_value()
        self.instr_pointer = new_pointer if not value else self.instr_pointer + 1


class LessThanOperation(IntcodeOperation):
    """Write 1 to index if the first value < second value."""
    def execute(self):
        self.output_to_index(1 if self.get_next_value() < self.get_next_value() else 0)
        self.instr_pointer += 1


class EqualsOperation(IntcodeOperation):
    """Write 1 to index if two values are equal."""
    def execute(self):
        self.output_to_index(1 if self.get_next_value() == self.get_next_value() else 0)
        self.instr_pointer += 1


class HaltOperation(IntcodeOperation):
    """Halt intcode processing."""
    def execute(self):
        self.halted = True


class AdjustRelativeBaseOperation(IntcodeOperation):
    """Adjust the relative base value."""
    def execute(self):
        self.relative_base += self.get_next_value()
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
            # Parse opcode
            opcode = self.intcode[self.instr_pointer] % 100
            # Execute operation and get output
            operation = OPERATIONS[opcode](self.intcode, self.instr_pointer, self.inputs, self.relative_base)
            output = operation.execute()
            # Update variables after operation
            self.instr_pointer = operation.instr_pointer
            self.relative_base = operation.relative_base
            self.halted = operation.halted
            if output is not None:
                self.output = output

    def set_inputs(self, *inputs):
        """Set one or more inputs."""
        self.inputs = [i for i in inputs]
        # Internally stored as reversed list, popping from beginning is slow
        self.inputs.reverse()

    @property
    def intcode_aslist(self):
        return [x for x in self.intcode.values()]
