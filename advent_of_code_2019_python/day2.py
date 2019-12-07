from typing import List
import click


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        intcode = f.read().rstrip('\n').split(',')
    return [int(x) for x in intcode]

@click.command()
@click.option('--input-file', required=True, type=str,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode = read_input(input_file)
    print(intcode)


if __name__ == '__main__':
    main()
