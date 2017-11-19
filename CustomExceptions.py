

class NoNoteException(Exception):
    def __init__(self, error_string: str) -> object:
        self.error_string = error_string