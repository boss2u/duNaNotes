from PyQt4.QtGui import QDialog, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QTextDocument, QTextCursor, QTextEdit


class FindDialog(QDialog):
    def __init__(self, page, parent=None, selectedText: str = ""):
        super().__init__(parent)
        # create the labels and the text edit for the dialog
        self.wordToFind = selectedText
        self.findLineEdit = QLineEdit()  # TODO: add find backward and forward buttons later
        self.matchCaseCheckBox = QCheckBox("Match &Case")
        self.wholeWordsCheckBox = QCheckBox("Whole &Words")
        # findButton = QPushButton("&Find")
        self.nextButton = QPushButton("&Next")
        self.previousButton = QPushButton("&Previous")
        self.document = page.document()  # page is a QTextEdit
        self.page = page

        if self.wordToFind and not self.wordToFind.isspace():
            self.findLineEdit.setText(self.wordToFind)
            self.findLineEdit.selectAll()

        # lay the dialog out
        layout = QHBoxLayout()
        layout.addWidget(self.findLineEdit)
        layout.addWidget(self.matchCaseCheckBox)
        layout.addWidget(self.wholeWordsCheckBox)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.previousButton)

        self.setLayout(layout)

        # signal slot connections
        self.previousButton.clicked.connect(self.findTextBackwards)
        self.nextButton.clicked.connect(self.findText)

    def findTextBackwards(self):
        self.findText(True)

    def findText(self, reverse: bool = False):
        """Selects the find pattern if found
           and changes the cursor position to the end of the search pattern
           if it is accepted
        """
        textToFind = self.findLineEdit.text()  # get the search term from the lineEdit
        if self.page is not None and isinstance(self.page, QTextEdit):
            if reverse:
                if self.matchCaseCheckBox.isChecked() and self.wholeWordsCheckBox.isChecked():
                    self.page.find(textToFind, QTextDocument.FindBackward |
                                   QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords)
                elif self.matchCaseCheckBox.isChecked():
                    self.page.find(textToFind, QTextDocument.FindBackward | QTextDocument.FindCaseSensitively)
                elif self.wholeWordsCheckBox.isChecked():
                    self.page.find(textToFind, QTextDocument.FindBackward | QTextDocument.FindWholeWords)
                else:
                    self.page.find(textToFind, QTextDocument.FindBackward)
            else:
                if self.matchCaseCheckBox.isChecked() and self.wholeWordsCheckBox.isChecked():
                    self.page.find(textToFind, QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords)
                elif self.matchCaseCheckBox.isChecked():
                    self.page.find(textToFind, QTextDocument.FindCaseSensitively)
                elif self.wholeWordsCheckBox.isChecked():
                    self.page.find(textToFind, QTextDocument.FindWholeWords)
                else:  # nothing is checked, just a normal search is demanded
                    self.page.find(textToFind)


                    # def findText(self, reverse:bool=False):
                    #     """Selects the find pattern if found
                    #        and changes the cursor position to the end of the search pattern
                    #        if it is accepted
                    #     """
                    #     textToFind = self.findLineEdit.text()  # get the search term from the lineEdit
                    #     if self.document is not None and isinstance(self.document, QTextDocument):
                    #         if reverse:
                    #             if self.matchCaseCheckBox.isChecked() and self.wholeWordsCheckBox.isChecked():
                    #                 self.selectFoundText( self.document.find(textToFind, , QTextDocument.FindBackward|
                    #                                    QTextDocument.FindCaseSensitively|QTextDocument.FindWholeWords))
                    #             elif self.matchCaseCheckBox.isChecked():
                    #                 self.selectFoundText( self.document.find(textToFind, 0, QTextDocument.FindCaseSensitively))
                    #             elif self.wholeWordsCheckBox.isChecked():
                    #                 self.selectFoundText(self.document.find(textToFind, 0, QTextDocument.FindWholeWords))
                    #         else:
                    #             if self.matchCaseCheckBox.isChecked() and self.wholeWordsCheckBox.isChecked():
                    #                 self.selectFoundText(self.document.find(textToFind, 0, QTextDocument.FindBackward|
                    #                                    QTextDocument.FindCaseSensitively|QTextDocument.FindWholeWords))
                    #             elif self.matchCaseCheckBox.isChecked():
                    #                 self.selectFoundText(self.document.find(textToFind, 0, QTextDocument.FindCaseSensitively))
                    #             elif self.wholeWordsCheckBox.isChecked():
                    #                 self.selectFoundText(self.document.find(textToFind, 0, QTextDocument.FindWholeWords))
                    #             else:  # nothing is checked, just a normal search is demanded
                    #                 self.page.find(textToFind)
                    # self.selectFoundText(self.document.find(textToFind))
                    # if self.matchCaseCheckBox.isChecked():
                    #     self.document.find(textToFind, 0, QTextDocument.FindCaseSensitively)
                    # if self.wholeWordsCheckBox.isChecked():
                    #     self.document.find(textToFind, 0, QTextDocument.FindWholeWords)

    def selectFoundText(self, cursor: QTextCursor):
        print(cursor.selectedText())
        cursor.select(QTextCursor.WordUnderCursor)
