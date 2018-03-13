from getpass import getpass
import re


class PasswordValidator(object):
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
                password_validator(self.password)
            )

    def __str__(self):
        return '<PasswordValidator>: {}'.format(self.password)

    def has_warnings(self):
        return True if len(self.warnings) > 0 else False

    def show_warnings(self):
        for warning in self.warnings:
            print(warning)


class ValidatorType(object):
    def __init__(self, password):
        self.weight = 1
        self.password = password

    def get_weight(self):
        return self.weight


class IsNotEmpty(ValidatorType):
    def validate(self):
        return True if self.password else False

    @staticmethod
    def warning():
        return 'The password cannot be empty'


class IsMinLen(ValidatorType):
    def validate(self):
        return True if len(self.password) >= 6 else False

    @staticmethod
    def warning():
        return 'The password should be more than 5 symbols'


class IsGoodLen(ValidatorType):
    def validate(self):
        return True if len(self.password) >= 8 else False

    @staticmethod
    def warning():
        return 'The password is less than eight characters'


class IsDuplicateCharacters(ValidatorType):
    def validate(self):
        return True if len(self.password) == len(set(self.password)) else False

    @staticmethod
    def warning():
        return 'The password has duplicate characters'


class IsUpperExist(ValidatorType):
    def validate(self):
        return True if re.search('[A-Z]', self.password) else False

    @staticmethod
    def warning():
        return 'Add please some symbols in upper register'


class IsLowerExist(ValidatorType):
    def validate(self):
        return True if re.search('[a-z]', self.password) else False

    @staticmethod
    def warning():
        return 'Add please some symbols in lower register'


class IsDigitExist(ValidatorType):
    def validate(self):
        return True if re.search('[\d]', self.password) else False

    @staticmethod
    def warning():
        return 'Add please some didgit'


class IsSymbolExist(ValidatorType):
    def validate(self):
        return True if re.search('[\W]', self.password) else False

    @staticmethod
    def warning():
        return 'Add please some symbol'


class CheckPasswInBadList(ValidatorType):
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
            return True if self.password.lower() not in self.bad_passwords else False

    def warning(self):
        if self.bad_passwords:
            return 'Password in bad passwords list'
        else:
            return 'File bad_passwords.txt Not Found'


def main():
    validator = PasswordValidator(getpass())
    validator.add_validators(
        IsNotEmpty,
        IsMinLen,
        IsGoodLen,
        IsDuplicateCharacters,
        IsUpperExist,
        IsLowerExist,
        IsDigitExist,
        IsSymbolExist,
        CheckPasswInBadList
    )
    rate = validator.validate()
    print('Your password rate is {}'.format(rate))
    if validator.has_warnings():
        validator.show_warnings()


if __name__ == '__main__':
    main()
