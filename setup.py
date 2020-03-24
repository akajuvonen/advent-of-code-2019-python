from setuptools import setup, find_packages


setup(
    name='advent-of-code-2019-python',
    version='0.14.0',
    description='Advent of Code 2019 solutions in Python',
    author='Antti Juvonen',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['click', 'attrs', 'numpy']
)
