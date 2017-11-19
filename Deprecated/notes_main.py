# This is the implementation or the client class
from PyQt4.QtGui import (QFileDialog, QDialog, QLineEdit, QTextDocument, QCheckBox, QPushButton, QHBoxLayout)

from View.notes_window import NotesMainWindow


class NotesMethods(NotesMainWindow):
    """This class does the background job of the whole  application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.page = None  # defines a new  scrollArea TODO: will be initialised to the first document, i.e, the one that is opened by default
        self.dialog = None  # will serve as a reference to keep the dialog alive to prevent it from being destroyed and hence garbage collected
        self.currentPage = None  # will hold the reference to the currently displayed page and it is a QTextEdit
        self.setCurrentPage()  # initialize the current page

    def fileNew(self):  # create a new note
        #self.page = notes_window.Container()  # self.page is now a QTextEdit object
        tabNumber = self.tabWidget.count()

        self.tabWidget.addTab(self.page, "Notes{}".format(tabNumber + 1))

    def closeEvent(self, e):
        pass  # TODO: grab the close event and do some background work before exiting the app:work include saving user settings

    def editInsert(self):
        mediaFile = QFileDialog.getOpenFileName(self, "Select Media File to Insert", "/home")

    def editPreferences(self):
        pass

    def editFind(self):
        if self.dialog is None:
            self.dialog = FindDialog(self, self.currentPage)  # pass FindDialog the page to
        self.dialog.show()  # find TODO: not sure this will work cause of self.page. RESOLVED
        self.dialog.raise_()
        self.dialog.activateWindow()

    def setCurrentPage(self):
        self.currentPage = self.tabWidget.currentWidget()  # get the current document

    def undo(self) -> object:
        """Connect to QTextEdit undo slot. A work around for inability to connect a QAction to
           QTextEdit undo slot.
        """
        self.currentPage.undoTriggered.connect(self.currentPage.undo)

    def redo(self):
        """Connect to QTextEdit undo slot. A work around for inability to connect a QAction to
            QTextEdit undo slot.
         """
        self.currentPage.redoTriggered.connect(self.currentPage.redo)


class FindDialog(QDialog):
    """This class Provides interface"""

    def __init__(self, page=None, parent=None):
        super().__init__(parent)
        self.findLineEdit = QLineEdit()
        self.matchCaseCheckBox = QCheckBox("Match &Case")
        self.wholeWordsCheckBox = QCheckBox("Whole &Words")
        # findButton = QPushButton("&Find")
        self.nextButton = QPushButton("&Next")
        self.previousButton = QPushButton("&Previous")
        self.document = page.document()  # page is a QTextEdit

        # TODO: add find backward and forward buttons later

        # lay the dialog out
        layout = QHBoxLayout()
        layout.addWidget(self.findLineEdit)
        layout.addWidget(self.matchCaseCheckBox)
        layout.addWidget(self.wholeWordsCheckBox)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.previousButton)

        self.setLayout(layout)

    def findText(self):
        """displays a find dialog, selects the find pattern if found
           and changes the cursor position to the end of the search pattern
           if it is accepted
        """
        textToFind = self.findLineEdit.text()  # get the search term from the lineEdit
        if self.document is not None and isinstance(self.document, QTextDocument):
            self.document.find(textToFind)
        if self.matchCaseCheckBox.isChecked():
            self.document.find(textToFind, 0, QTextDocument.FindCaseSensitively)
        if self.wholeWordsCheckBox.isChecked():
            self.document.find(textToFind, 0, QTextDocument.FindWholeWords)
