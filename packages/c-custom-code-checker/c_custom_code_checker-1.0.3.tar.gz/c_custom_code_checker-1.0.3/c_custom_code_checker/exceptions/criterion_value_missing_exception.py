class CriterionValueMissingException(Exception):
    def __init__(self):
        self.message = 'Criterion value not informed'

    def __str__(self):
        return self.message 