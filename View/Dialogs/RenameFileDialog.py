import os
from PyQt4.QtGui import QDialog, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout,QTextDocument, QLabel
# from ..notes_window import applicationDirectory

# TODO: This dialog has to validate its input. It has to make sure empty strings \
# TODO: are not used as file names.
# TODO: It has to make sure invalid characters are not used as filenames

applicationDirectory = os.environ["HOME"] + "/.Notes"  # set application directory TODO: remove this later


class RenameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.newNameLabel = QLabel("New _Name")
        self.newNameLineEdit = QLineEdit()
        self.newNameLabel.setBuddy(self.newNameLineEdit)
        self.okButton = QPushButton("O&K")
        self.cancelButton = QPushButton("&Cancel")
        self.cancelButton.setDefault(True)

        self.newNameLineEdit.setText(applicationDirectory)
        self.newNameLineEdit.selectAll()

        layout = QVBoxLayout(self)
        layout.addWidget(self.newNameLabel)
        layout.addWidget(self.newNameLineEdit)

        miniLayout = QHBoxLayout()
        miniLayout.addWidget(self.okButton)
        miniLayout.addWidget(self.cancelButton)

        layout.addLayout(miniLayout)

        self.setLayout(layout)

        self.cancelButton.clicked.connect(self.reject)
        self.okButton.clicked.connect(self.accept)

    def getNewName(self):
        return self.newNameLineEdit.text()

    def accept(self) :
        if self.newNameLineEdit.text() == "":
            self.okButton.setEnabled(False)
            self.newNameLineEdit.setFocus()
        super().accept()