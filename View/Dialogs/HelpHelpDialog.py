from PyQt4.QtGui import QDialog, QLabel, QPushButton, QVBoxLayout


help_text = """
                        Click on New or Press Ctrl+N to create a new note
                        Notes are auto saved. No need to explicitly save a note
                        
                        To rename a note, go to Edit->Rename Note . Select the 
                        new name for the note and accept the changes made by 
                        pressing OK or cancel by pressing cancel or Escape button
                        on the keyboard.
                        
                        To find a text in a note book, go to edit->Find  or press 
                        Ctrl+F. Enter the find text and press Next to find forward from
                        the current cursor position of Previous to find backward from
                        the current previous position. Check the the check boxes for 
                        Match case and Whole words to perfom a case sensitive search
                        and find whole words respectively.                        
                """


class HelpHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        text_label = QLabel()
        text_label.setText(help_text)
        okButton = QPushButton("&OK")

        layout = QVBoxLayout(self)
        layout.addWidget(text_label)
        layout.addWidget(okButton)

        self.setWindowTitle("duNaNotes Help")
        okButton.clicked.connect(self.close)


        # create the labels and buttons for the dialog