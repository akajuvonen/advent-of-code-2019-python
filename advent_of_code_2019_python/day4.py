from typing import Optional

import click

MIN_VALUE = 108457
MAX_VALUE = 562041


def _validate_passwd(passwd: str, group_size: Optional[int] = None) -> bool:
    if len(passwd) != 6 or any(passwd[i] > passwd[i+1] for i in range(5)):
        return False
    uniques = set(passwd)
    # If there are no decreasing digits, identical digits must always be next to
    # each other. If number of unique digits is the same passwd length, we don't
    # have a sequence of two identical digits.
    if len(uniques) < len(passwd):
        # One of the adjacent identical digit groups must be 2 digits exactly
        if group_size and any(passwd.count(c) == group_size for c in uniques):
            return True
    return False


def calculate_n_passwords(min_value: int, max_value: int) -> int:
    """Calculates the number of acceptable passwords.

    Rules: Digits never decrease, 6 digits, two adjacent digits the same.

    Arguments:
        min_value: Minimum value for a password
        max_value: Maximum password number

    Returns:
        number of acceptable passwords between min and max
    """
    n_passwords = 0
    for passwd in range(min_value, max_value + 1):
        if _validate_passwd(str(passwd), 2):
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
