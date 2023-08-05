class RuleMissingCriterionException(Exception):
    def __init__(self):
        self.message = 'Missing rule criterion'

    def __str__(self):
        return self.message 