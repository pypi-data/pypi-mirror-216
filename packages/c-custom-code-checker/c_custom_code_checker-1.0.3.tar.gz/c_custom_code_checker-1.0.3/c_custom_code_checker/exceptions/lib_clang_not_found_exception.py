class LibClangNotFoundException(Exception):
    def __init__(self):
        self.message = 'libclang not found'

    def __str__(self):
        return self.message     