import sys
from PyQt4.QtGui import QMainWindow, QApplication
from View.notes_window import NotesMainWindow
from Model.Note import Note

class Controller(QMainWindow):
    """The controlller class"""
    _model = None  # The model
    _view = None  # reference to the view


    def __init__(self, parent=None, view:NotesMainWindow = None):
        super().__init__(parent)
        self.view = view
        self.setCentralWidget(self.view)

    def __init__(self, view:NotesMainWindow, model:Note):
        self.view = view
        self.model = model
    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value:NotesMainWindow):
        """
        :type value: NotesMainWindow
        """
        if isinstance(value, NotesMainWindow):
            self._view = value

    @property
    def model(self):
        return self._model

    @model.setter
    def (self, value:Note):
        self._model = value
app = QApplication(sys.argv)
controller = Controller(view=NotesMainWindow())
controller.show()
app.exec_()