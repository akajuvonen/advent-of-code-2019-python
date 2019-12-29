from setuptools import setup, find_packages


setup(
    name='advent-of-code-2019-python',
    version='0.4.1',
    description='Advent of Code 2019 solutions in Python',
    author='Antti Juvonen',
    packages=find_packages(),
    install_requires=['click', 'attr']
)
