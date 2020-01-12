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

    zeros_in_layers = np.array([layer.size - np.count_nonzero(layer) for layer in image])
    fewest_zeros_layer_idx = np.argmin(zeros_in_layers)
    fewest_zeros_layer = image[fewest_zeros_layer_idx]
    ones = np.count_nonzero(fewest_zeros_layer == 1)
    twos = np.count_nonzero(fewest_zeros_layer == 2)
    print("Number of digits 1 and 2 multiplied (in the layer with fewest 0 digits:)")
    print(ones * twos)


if __name__ == '__main__':
    main()
