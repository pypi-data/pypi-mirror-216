class CriterionNotRespectedException(Exception):
    def __init__(self,msg):
        self.message = f'Criterion not respected to {msg}'

    def __str__(self):
        return self.message 