from advent_of_code_2019_python.day8 import generate_image
import numpy as np


def test_generate_image():
    input_image = np.array([[[0, 2], [2, 2]], [[1, 1], [2, 2]], [[2, 2], [1, 2]], [[0, 0], [0, 0]]])
    expected_image = np.array([[0, 1], [1, 0]])
    assert np.array_equal(generate_image(input_image), expected_image)
