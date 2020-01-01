import click

from advent_of_code_2019_python import IntcodeComputer
from itertools import permutations


def calculate_max_thruster_signal(intcode_computer: IntcodeComputer) -> int:
    max_thruster_signal = 0
    for permutation in permutations(range(5)):
        output = 0
        for phase_setting in permutation:
            intcode_computer.compute(inputs=[phase_setting, output])
            output = intcode_computer.output[0]
            intcode_computer.reset()
        final_thruster_signal = output
        if final_thruster_signal > max_thruster_signal:
            max_thruster_signal = final_thruster_signal
    return max_thruster_signal


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day7.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    max_thruster_signal = calculate_max_thruster_signal(intcode_computer)
    print(max_thruster_signal)


if __name__ == '__main__':
    main()
