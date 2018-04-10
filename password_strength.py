import re
from getpass import getpass


def check_for_empty_password(password: str) -> bool:
    return bool(password)


def check_for_min_len_of_password(password: str, min_len=6) -> bool:
    return len(password) >= min_len


def check_for_good_len_of_password(password: str, min_len=8) -> bool:
    return len(password) >= min_len


def check_for_same_symbols(password: str) -> bool:
    return len(password) == len(set(password))


def check_for_upper_case(password: str) -> bool:
    return bool(re.search('[A-Z]', password))


def check_for_lower_case(password: str) -> bool:
    return bool(re.search('[a-z]', password))


def check_for_digits(password: str) -> bool:
    return bool(re.search('[\d]', password))


def check_for_symbols(password: str) -> bool:
    return bool(re.search('[\W]', password))


def load_bad_passwords(file_path='bad_passwords.txt'):
    try:
        with open(file_path, 'r') as file_handler:
            return file_handler.read().split(sep='\n')
    except FileNotFoundError:
        return None


def check_if_bad_password(
                        password: str,
                        bad_passwords: str,
                        rate_count: int=2) -> int:
    if bad_passwords:
        if password.lower() not in bad_passwords:
            return rate_count
        else:
            return -rate_count
    else:
        return False


def main():
    password = getpass()
    bad_passwords = load_bad_passwords()
    checklist = (
        check_for_empty_password(password),
        check_for_min_len_of_password(password),
        check_for_good_len_of_password(password),
        check_for_same_symbols(password),
        check_for_upper_case(password),
        check_for_lower_case(password),
        check_for_digits(password),
        check_for_symbols(password),
        check_if_bad_password(password, bad_passwords),
    )
    password_rate = sum(checklist)
    print(checklist)
    print('The password evaluation should be read as follows:',
          '\n1 is the lowest rate. We strongly recommend to change a ',
          '1 - rated password;\n5 is a mediocre rate',
          '\n10 is the highest rate, meaning your password is strong enough.')
    print('your password rate = ', password_rate)


if __name__ == '__main__':
    main()
