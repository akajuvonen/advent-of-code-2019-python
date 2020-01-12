import click
import numpy as np  # type: ignore


def load_image(filename: str, width: int, height: int) -> np.ndarray:
    """Load an image text file into numpy array with x layers.
    Each layer has specified width and height.

    Arguments:
        filename: Filename to open.
        width: width of each image layer
        height: height of each layer

    Returns:
        Array with each layer separated.
    """
    with open(filename) as f:
        image = np.array([int(x) for x in f.read().rstrip('\n')])
    return image.reshape((-1, height, width))


def image_corruption_check(image: np.ndarray) -> int:
    """Returns a checksum to see if an image is corrupted.
    This is done by first finding the layer with fewest zeros.
    Then, the number of ones is multiplied by number of twos, and this
    value is returned.

    Arguments:
        image: Array with image pixel information on each layer

    Returns:
        Image checksum.
    """
    zeros_in_layers = np.array([layer.size - np.count_nonzero(layer) for layer in image])
    fewest_zeros_layer_idx = np.argmin(zeros_in_layers)
    fewest_zeros_layer = image[fewest_zeros_layer_idx]
    ones = np.count_nonzero(fewest_zeros_layer == 1)
    twos = np.count_nonzero(fewest_zeros_layer == 2)
    return ones * twos


def generate_image(image: np.ndarray) -> np.ndarray:
    return np.array([1, 2, 3])


@click.command()
@click.option('--input-file', required=True, type=str, default='inputs/input_day8.txt', show_default=True,
              help='Path to image file encoded in Space Image Format')
def main(input_file):
    width = 25
    height = 6
    image = load_image(input_file, width, height)

    print("Image checksum:")
    print(image_corruption_check(image))


if __name__ == '__main__':
    main()
