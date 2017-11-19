from unittest import TestCase
from View.Dialogs.FindDialog import FindDialog


class Dialogs(TestCase):
    def __init__(self):
        self.setUp()
        super().__init__()

    def test_onFind(self):
        self.fail()

    def setUp(self):
        self.find_dialog = FindDialog()
        super().setUp()
