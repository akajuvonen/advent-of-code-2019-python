import click
import numpy as np


def load_image(filename, width, height):
    with open(filename) as f:
        image = np.array([int(x) for x in f.read().rstrip('\n')])
    return image.reshape((-1, height, width))


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day8.txt', show_default=True,
              help='Path to image file encoded in Space Image Format')
def main(input_file):
    width = 25
    height = 6
    image = load_image(input_file, width, height)


if __name__ == '__main__':
    main()
