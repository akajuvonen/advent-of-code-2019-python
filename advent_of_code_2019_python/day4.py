import click
from typing import Optional


MIN_VALUE = 108457
MAX_VALUE = 562041


def _validate_passwd(passwd: str, group_size: int = 2) -> bool:
    if len(passwd) != 6 or any(passwd[i] > passwd[i+1] for i in range(5)):
        return False
    uniques = set(passwd)
    if len(uniques) < len(passwd):
        if group_size and any(passwd.count(c) == group_size for c in uniques):
            return True
    return False


def calculate_n_passwords(min_value: int, max_value: int) -> int:
    n_passwords = 0
    for passwd in range(min_value, max_value + 1):
        if _validate_passwd(str(passwd)):
            n_passwords += 1
    return n_passwords


@click.command()
@click.option('--min-value', required=True, type=int, default=MIN_VALUE, show_default=True,
              help='Minimum value for password')
@click.option('--max-value', required=True, type=int, default=MAX_VALUE, show_default=True,
              help='Maximum value for password')
def main(min_value, max_value):
    password_count = calculate_n_passwords(min_value, max_value)
    print(password_count)


if __name__ == '__main__':
    main()
