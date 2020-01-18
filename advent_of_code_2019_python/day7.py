import copy
from itertools import permutations
from typing import Optional

import click

from advent_of_code_2019_python import IntcodeComputer


def calculate_max_thruster_signal_feedback(intcode_computer: IntcodeComputer) -> Optional[int]:
    """
    Calculates maximum thruster signal that can be obtained with some combination of amplifier phase settings
    using a feedback loop.

    The computer will keep computing without stopping until waiting for input, or they just output something. When the
    final amplifier halts, the program is done and the last output is the thruster signal.

    Like the non-feedback version, different permutation of phase settings are attempted and maximum thruster signal
    is returned.

    Arguments:
        intcode_computer: Intcode computer loaded with the correct program. This will be coped to all amplifiers.

    Returns:
        Maximum amplified thruster signal.
    """
    max_thruster_signal = None
    for permutation in permutations(range(5, 10)):
        # Initialize all computers
        computers = []
        output = 0
        for phase_setting in permutation:
            new_computer = copy.deepcopy(intcode_computer)
            new_computer.set_inputs(phase_setting, output)
            new_computer.compute()
            output = new_computer.output
            computers.append(new_computer)
        # Continue the feedback loop until halt
        halted = False
        while True:
            if halted:
                final_thruster_signal = output
                break
            for computer in computers:
                computer.set_inputs(output)
                computer.compute()
                if computer.halted:
                    halted = True
                    break
                output = computer.output
        if max_thruster_signal is None or final_thruster_signal > max_thruster_signal:
            max_thruster_signal = final_thruster_signal
    return max_thruster_signal


def calculate_max_thruster_signal(intcode_computer: IntcodeComputer) -> Optional[int]:
    """
    Calculates max thruster signal using connected intcode computers with some permutations of phase setting.

    Arguments:
        intcode_computer: Intcode computer loaded with the correct program.

    Returns:
        Maximum signal that can be obtained with some permutation of phase settings.
    """
    max_thruster_signal = None
    for permutation in permutations(range(5)):
        output = 0
        for phase_setting in permutation:
            new_computer = copy.deepcopy(intcode_computer)
            new_computer.set_inputs(phase_setting, output)
            new_computer.compute()
            output = new_computer.output
        final_thruster_signal = output
        if max_thruster_signal is None or final_thruster_signal > max_thruster_signal:
            max_thruster_signal = final_thruster_signal
    return max_thruster_signal


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day7.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    max_thruster_signal = calculate_max_thruster_signal(intcode_computer)
    print(max_thruster_signal)

    intcode_computer = IntcodeComputer.from_file(input_file)
    max_thruster_signal_feedback = calculate_max_thruster_signal_feedback(intcode_computer)
    print(max_thruster_signal_feedback)


if __name__ == '__main__':
    main()
