from PyQt4.QtGui import QDialog, QGridLayout, QCheckBox, QPushButton, QHBoxLayout, QTextDocument, QLabel

class HelpAboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        myNameLabel1 = QLabel("duNaNotes")
        myNameLabel2 = QLabel("by duNaMis")
        versionLabel = QLabel("Version 0.1")
        okButton = QPushButton("&Ok")

        layout = QGridLayout()
        layout.addWidget(myNameLabel1, 0, 0, 2, 2)
        layout.addWidget(myNameLabel2, 3, 2, 1, 1)
        layout.addWidget(versionLabel, 4,3, 1, 1)
        layout.addWidget(okButton, 5, 3, 1, 2)

        okButton.setFocus()
        self.setLayout(layout)

        self.setWindowTitle("duNaNotes")

        # signal slot connections
        okButton.clicked.connect(self.close)
