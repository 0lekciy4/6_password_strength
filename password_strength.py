import re
from getpass import getpass


def load_bad_passwords(file_path):
    with open(file_path, 'r') as file_handler:
        return file_handler.read().split(sep='\n')


def check_in_bad_passwords_list(password):
    bad_passwords_list = load_bad_passwords('bad_passwords.txt')
    if password.lower() not in bad_passwords_list:  # т.к. в словаре только строчные символы
        return 1
    return -3


def check_in_patterns(password):
    password_in_pattern = 0
    for pattern in ('[a-z]', '[A-Z]', '\d', '\W'):
        if re.findall(pattern, password):
            password_in_pattern += 1
    return password_in_pattern


def check_len(password):
    if len(password) >= 8:
        return 4
    elif len(password) >= 6:
        return 2
    else:
        return -2


def check_for_duplicate_characters(password):
    if len(password) == len(set(password)):
        return 1


def get_password_strength(password):
    password_strength = 0
    check_password = [
        check_for_duplicate_characters(password),
        check_in_bad_passwords_list(password),
        check_in_patterns(password),
        check_len(password),
    ]
    for check_weight in check_password:
        if check_weight is not None:
            password_strength += check_weight
    return password_strength


if __name__ == '__main__':
    password = getpass('Input your password for check strenght:')
    password_strength = get_password_strength(password)
    print('Password strength = {}'.format(password_strength))
