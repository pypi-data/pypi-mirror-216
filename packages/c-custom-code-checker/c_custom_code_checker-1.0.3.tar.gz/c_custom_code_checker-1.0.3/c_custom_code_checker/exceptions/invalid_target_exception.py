
class InvalidTargetException(Exception):
    def __init__(self):
        self.message = 'Invalid target value'

    def __str__(self):
        return self.message 