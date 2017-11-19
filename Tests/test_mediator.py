import unittest
from unittest.case import TestCase
from MITM.Mediator import Mediator


class Mediator_Test(TestCase):

    def __init__(self):
        super().__init__()
        self.mediator = Mediator()

    def test_checkIfNoteExists_fedAnExistingNote_ReturnsTrue(self):
        pass

    def test_checkIfNoteExists_fedNoneExistingNote_ReturnsFalse(self):
        pass

    def test_createNote_runNormally_returnsNewNoteObject(self):
        pass

    def test_createNote_runAbnormally_throwsAnException(self):
        pass

    def test_saveNote_runWhileThereisCurrentlyDisplayedNote_savesTheNote(self):
        pass

    def test_saveNote_runWhileCurrentlyDisplayedNoteIsNone_raisesAnException(self):
        pass

    def test_saveNote_givenAlreadyExistingNote_raisesFileExistException(self):
        pass

    def test_renameNote_triesToRenameANoteToANameThatDoesntExistYet_sucessfull(self):
        pass

    def test_renameNote_triesToRenameANoteToANameThatAlreadytExist_raisesAnException(self):
        pass

    def test_openCurrentNote_triesToOpenAnExistingNoteForReading_succeeds(self):
        pass

    def test_openCurrentNote_triesToOpenANonExistingNoteForReading_raisesException(self):
        pass

    def test_setCurrentlyDisplayedNote_triesToSetCurrentlyDisplayedNoteToANoteObject_succeeds(self):
        pass

    def test_setCurrentlyDisplayedNote_triesToSetCurrentlyDisplayedNoteNotToANoteObject_raisesAnException(self):
        pass


if __name__ == '__main__':
    unittest.Main()