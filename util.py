from enum import Enum

class Message(Enum):
    OK = 'OK\n'
    Error = 'ERROR\n'
    Fail = 'FAIL\n'

    def __str__(self):
        return self.value

class InputError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
