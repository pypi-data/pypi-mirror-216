
class RuleMissingTargetException(Exception):
    def __init__(self):
        self.message = 'Missing rule target'

    def __str__(self):
        return self.message 