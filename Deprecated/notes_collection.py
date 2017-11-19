#The collection class for Notes
from Model.Note import Note

class NotesCollection(object):
    """A part of the mode"""
    _notes = []
    def __init__(self, notes:list=[]):
        self.notes = notes

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value:list):
        self._notes = value

