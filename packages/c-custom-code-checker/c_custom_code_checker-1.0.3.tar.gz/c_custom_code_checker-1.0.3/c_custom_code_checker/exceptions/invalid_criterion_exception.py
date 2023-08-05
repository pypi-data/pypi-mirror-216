
class InvalidCriterionException(Exception):
    def __init__(self):
        self.message = 'Invalid criterion value'

    def __str__(self):
        return self.message 