""" Model definitions """
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """ Defines user blueprint """
    __id = None

    def __init__(self, email, password, name, deposit):
        """ Initializes user object """
        self.__id = uuid.uuid4()
        self.email = email.lower()
        self.password_hash = generate_password_hash(password)
        self.name = name.title()
        self.__balance = deposit
        # self.expenses = []

        with open("data/user_data.txt", 'w+') as f:
            f.write(f"Email:{email}, Password:{password}, Name:{name}, Deposit:{self.__balance}\n")
        with open("emails.txt", 'w+') as mails:
            mails.write(email + '\n')

    def check_password(self, password):
        """ Compares password hash with password """
        return check_password_hash(self.password_hash, password)

    def get_balance(self):
        """ Returns account balance """
        return self.__balance

    def topup(self, amount):
        """ Adds specified amount to current balance """
        try:
            self.__balance += amount
            with open("data/user_data.txt", 'r') as f:
                lines = f.readlines()
                lines[self.__id] = f"Email:{self.email}, Password:{self.password}, Name:{self.name}, Deposit:{self.__balance}\n"
            with open("data/user_data.txt", "w") as F:
                F.writelines(lines + "\n")
                F.close()
            return True
        except:
            return False

    @property
    def id(self):
        """ Returns user id property """
        return self.__id