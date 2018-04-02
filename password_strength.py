import re
from getpass import getpass


class PasswordValidator:
    def __init__(self, password):
        self.password = password
        self.warnings = []
        self.validators = []
        self.weight = 0

    def validate(self):
        self.weight, self.warnings = 0, []
        for password_validator in self.validators:
            if password_validator.validate():
                self.weight += password_validator.weight
            else:
                self.warnings.append(password_validator.warning())
        return self.weight

    def add_validators(self, *args):
        for password_validator in args:
            self.validators.append(
                password_validator(self.password),
            )

    def __str__(self):
        return '<PasswordValidator>: {}'.format(self.password)

    def has_warnings(self):
        return len(self.warnings) > 0

    def show_warnings(self):
        for warning in self.warnings:
            print(warning)


class BaseValidator:
    def __init__(self, password):
        self.weight = 1
        self.password = password

    def get_weight(self):
        return self.weight


class NotEmptyChecker(BaseValidator):
    def validate(self):
        return bool(self.password)

    @staticmethod
    def warning():
        return 'The password cannot be empty'


class MinLenChecker(BaseValidator):
    def validate(self):
        self.min_len = 6
        return len(self.password) >= self.min_len

    @staticmethod
    def warning():
        return 'The password should be more than 5 symbols'


class GoodLenChecker(BaseValidator):
    def validate(self):
        self.good_len = 8
        return len(self.password) >= self.good_len

    @staticmethod
    def warning():
        return 'The password is less than eight characters'


class DuplicateCharactersChecker(BaseValidator):
    def validate(self):
        return len(self.password) == len(set(self.password))

    @staticmethod
    def warning():
        return 'The password has duplicate characters'


class UpperExistChecker(BaseValidator):
    def validate(self):
        return bool(re.search('[A-Z]', self.password))

    @staticmethod
    def warning():
        return 'Add please some symbols in upper register'


class LowerExistChecker(BaseValidator):
    def validate(self):
        return bool(re.search('[a-z]', self.password))

    @staticmethod
    def warning():
        return 'Add please some symbols in lower register'


class DigitExistChecker(BaseValidator):
    def validate(self):
        return bool(re.search('[\d]', self.password))

    @staticmethod
    def warning():
        return 'Add please some didgit'


class SymbolExistChecker(BaseValidator):
    def validate(self):
        return bool(re.search('[\W]', self.password))

    @staticmethod
    def warning():
        return 'Add please some symbol'


class PasswInBadListChecker(BaseValidator):
    def __init__(self, password):
        self.password = password
        self.weight = 2
        self.file_path = 'bad_passwords.txt'
        self.bad_passwords = self.load_bad_passwords()

    def load_bad_passwords(self):
        try:
            with open(self.file_path, 'r') as file_handler:
                return file_handler.read().split(sep='\n')
        except FileNotFoundError:
            return None

    def validate(self):
        if self.bad_passwords:
            return self.password.lower() not in self.bad_passwords

    def warning(self):
        if self.bad_passwords:
            return 'Password in bad passwords list'
        else:
            return 'File bad_passwords.txt Not Found'


def main():
    validator = PasswordValidator(getpass())
    validator.add_validators(
        NotEmptyChecker,
        MinLenChecker,
        GoodLenChecker,
        DuplicateCharactersChecker,
        UpperExistChecker,
        LowerExistChecker,
        DigitExistChecker,
        SymbolExistChecker,
        PasswInBadListChecker,
    )
    rate = validator.validate()
    print('Your password rate is {}'.format(rate))
    if validator.has_warnings():
        validator.show_warnings()


if __name__ == '__main__':
    main()
