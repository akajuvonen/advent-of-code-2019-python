import time

import click
import numpy as np  # type: ignore

from advent_of_code_2019_python import IntcodeComputer


def _array_formatter(x):
    icons = {1: '#',
             2: 'X',
             3: '_',
             4: 'O'}
    return icons[x] if x in icons else '.'


def _get_paddle_input(paddle_x, ball_x):
    if ball_x < paddle_x:
        return -1
    elif ball_x > paddle_x:
        return 1
    else:
        return 0


def play_game(intcode_computer: IntcodeComputer, screen: np.ndarray, show: bool = False):
    # play for free by settings first intcode address to 2
    intcode_computer.intcode[0] = 2
    score = 0
    paddle_x = 0
    ball_x = 0
    i = 0
    tile_count = screen.shape[0] * screen.shape[1]

    np.set_printoptions(formatter={'all': _array_formatter}, linewidth=100)

    while not intcode_computer.halted:
        x = intcode_computer.compute()
        y = intcode_computer.compute()
        output = intcode_computer.compute()
        if x == -1 and y == 0:
            score = output
        else:
            if x is not None and y is not None:
                screen[y][x] = output
                if output == 3:
                    paddle_x = x
                elif output == 4:
                    ball_x = x
                intcode_computer.set_inputs(_get_paddle_input(paddle_x, ball_x))
        i += 1
        if show:
            # start drawing only when the screen is fully populated
            if i > tile_count:
                print(screen)
                print(score)
                time.sleep(0.05)
    return score


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day13.txt', show_default=True,
              help='Path to file containing Intcode program (comma-separated list)')
def main(input_file):
    intcode_computer = IntcodeComputer.from_file(input_file)
    tiles = {}
    while not intcode_computer.halted:
        x = intcode_computer.compute()
        y = intcode_computer.compute()
        tile = intcode_computer.compute()
        if x is not None and y is not None:
            tiles[(x, y)] = tile
    print(f' Number of block tiles on the screen: {list(tiles.values()).count(2)}')

    # Get screen size
    max_x, max_y = 0, 0
    for x, y in tiles:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    score = play_game(IntcodeComputer.from_file(input_file), np.zeros((max_y + 1, max_x + 1), dtype=np.int8))
    print(f'Score: {score}')


if __name__ == '__main__':
    main()
