# This class represents the controller or presenter or the viewModel
import os
import View
import Model.Note
from  CustomExceptions import  NoNoteException
# from View.notes_main import FindDialog
from Model.Note import Note
from View.Dialogs.FindDialog import FindDialog
from View.TabbedPage import TabbedPage
# from View.notes_window import applicationDirectory


class Mediator(object):
    """This class serves as the layer of  abstraction between the view and the model
            It makes sure that the view does not know about or depend upon the model
            All routes of communication of between the model and the view goes through the model
    """
    def __init__(self, notes_collection = []):
        self.dialog = None  # pass FindDialog the page to
        self.notesCollection = []  # the collection of notes for the application
        self.currentlyDisplayedNote = None

    # region Methods
    def saveNote(self, text:str, note:Note=None):  # TODO: do this in another thread
        if note and isinstance(note, Note):
            try:
                path = note.NotePath
                with open(path, "w") as file_handle:
                    file_handle.write(text)
                print("Note Saved Successfully")
                return
            except IOError as e:
                raise e

        # this is now redundant
        elif self.currentlyDisplayedNote:  # and not self.checkIfNoteExists(self.currentlyDisplayedNote.NotePath):
            try:
                path = self.currentlyDisplayedNote.NotePath
                # if self.checkIfNoteExists(path):
                #     raise FileExistsError("???>>>This file exits before. Give it another name")
                with (open(path, "w")) as file_handle:
                    file_handle.write(text)  # save the text
                print("Note Saved successfully")
                return
            # except FileExistsError as e:
            #     print(e)
            except IOError as error:
                raise error

        raise NoNoteException("No attached note")

    def renameNote(self, new_name:str):
        note_name = os.path.normpath(os.path.join(applicationDirectory, new_name))
        try:
            if not self.checkIfNoteExists(note_name+".dn"):
                os.rename(self.currentlyDisplayedNote.NotePath, "{}".format(note_name+".dn"))  # TODO: this has to be better...like seriously!!!
        # except FileNotFoundError:
        except IOError as e:
            print("Couldn't rename the note: ", e)
            raise e

    def createNote(self, numberOfNotes: int=0, name:str="", notePath:str="") -> Model.Note:
        """Create a Note Object from the filename given
            Adds the created note to the notesCollection list
            Returns the created note"""
        noteName = ""
        if notePath:
            noteName = os.path.basename(notePath).rsplit(".", 1)[0]
        else:
            noteName = "Note " + format(numberOfNotes) \
                if name.isspace() or name == "" else name  # format() converts the int to string. Could have also used str(numberOfNotes)
            notePath = os.path.join(applicationDirectory ,  noteName)+".dn"
        print("\nNote Path is :  ", notePath)
        createdNote = Model.Note.Note(noteName, notePath)
        self.notesCollection.append(createdNote)
        self.setCurrentlyDisplayedNote(createdNote)
        return createdNote

    def setCurrentlyDisplayedNote(self, note:Note):
        if isinstance(note, Note):
            self.currentlyDisplayedNote = note  # TODO: synchronisation with currently displayed page needed
            print("I have been notified of a change in current note")
            return
        raise TypeError("Expected a Note Object, got a {}".format(type(note)))

    # def editFind(self):
    #     if self.dialog is None:
    #         self.dialog = FindDialog(self, self.currentPage)
    #     self.dialog.show()  # find TODO: not sure this will work cause of self.page. RESOLVED
    #     self.dialog.raise_()
    #     self.dialog.activateWindow()

    @property
    def NotesCollection(self) -> list:
        return self.notesCollection

    @NotesCollection.setter
    def NotesCollection(self, value):
        if value not in self.notesCollection and type(value) == Note :
            self.notesCollectionnotesCollection.append(value)

    def checkIfNoteExists(self, note_path):
        return os.path.exists(note_path)

    def openCurrentNote(self):  # TODO: maybe 'open' better describes this method: Handled
        try:
            with open(self.currentlyDisplayedNote.NotePath, "r") as f:
                lines = f.read()
                return lines
        except IOError as e:
            raise e

    @staticmethod
    def returnNotePath(note:Note):
        return note.NotePath

# end region

homeFolder = os.environ["HOME"]
applicationDirectory = homeFolder+"/.Notes"



