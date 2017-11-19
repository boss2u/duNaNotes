import logging
from PyQt4.QtGui import QTextEdit, QTextCursor
from PyQt4.QtCore import  pyqtSignal
from Model.Note import Note
import MITM.Mediator


class TabbedPage(QTextEdit):
    """ A text edit that has a note object attached
        This class provides editing areas for the QTabWidget
        It provides the pages
    """
    __redoT = pyqtSignal(name="redoT")
    __redoTriggered = pyqtSignal(name="redoTriggered")
    __undoTriggered = pyqtSignal(name="undoTriggered")  # signal to indicate that an undo operation is needed.
    __firstTime = pyqtSignal(name="FirstTime")  # signal that indicates the page has been navigated to the first time
    __dirty = False  # A change tracker

    __page_number = 0  # works in conjunction with undo() in class NotesMethods
    __navigationCount = 0  # counts the number of times a page has been naved to
    __isCurrentPage = False

    def __init__(self, parent=None, note:Note=None):  # TODO: implement an autosave feature for this class
        super().__init__(parent)
        # self.page_number += 1  # TODO: maybe let the parent widget(TabWidget) assign the page number; Done
        # self.numCreation()  # gives the number of this page among pages.
        assert isinstance(note, Note)
        self.note = note
        self.mediator = parent.mediator

        self.textChanged.connect(self.changedSomething)
        # self.firstTime.connect(self.something)
        self.firstTime.connect(parent.openPageOnFirstNavigation)

    # def openFirst(self):
    #     """Reads the content of the file on first nav.
    #         Implements something like lazy loading
    #         Implementation is whack.
    #         Implementation Path:
    #             onWindowStart -> createNoteObjectFromNoteFile -> createAndLoadNotes ->
    #             loadNotes -> openPageOnFirstNavigation
    #         TODO: make a better lazy loading implementatiion"""
    #     # TODO: make a better lazy loading implementatiion
    #     print("\n<<<<<I also work\n")
    #     contents = self.mediator.openCurrentPage()
    #     self.setHtml(contents)

    def something(self):
        print("\n>>>> Huh, I worked!!!\n")

    def getNote(self):
        return self.note    # note is of type Mediator.Note

    def changedSomething(self):
        logging.info("I have been called, so something has been changed")
        self.dirty = True
        self.__redoT.emit()

    @property
    def dirty (self):
        return self.__dirty
    @dirty.setter
    def dirty(self, value:bool):
        if isinstance(value, bool):
            self.__dirty = value

    def checkFirstTime(self):
        if self.navigationCount == 1:
            self.firstTime.emit()

    def I_becameCurrentPage(self):
        self.isCurrentPage = True
        self.navigationCount += 1
        self.checkFirstTime()
    # @classmethod
    # def numCreation(cls):
    #     cls.__page_number += 1

    @property
    def isCurrentPage(self):
        return self.__isCurrentPage
    @isCurrentPage.setter
    def isCurrentPage (self, value):
        if isinstance(value, bool):
            self.__isCurrentPage = value

    @property
    def firstTime(self):
        return self.__firstTime
    @firstTime.setter
    def firstTime(self, value):
        self.__firstTime = value

    @property
    def navigationCount(self):
        return self.__navigationCount
    @navigationCount.setter
    def navigationCount(self, value:int):
        if isinstance(value, int):
            self.__navigationCount = value

    @property
    def page_number(self):
        return self.__page_number
    @page_number.setter
    def page_number(self, value:int):
        if isinstance(value, int):
            self.__page_number = value

    def getDocumentCursor(self):
        """Returns the text cursor associated with the document
        """
        cursor = self.textCursor()  # get the QTextCursor with this page as its associated document. Note:
        return cursor  # this can be moved inside the constructor
