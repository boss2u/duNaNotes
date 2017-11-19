# This represents the model
import time, os


class Note(object):
    """This class represents the model for the application. A note is the unit of data for the application
    """
    def __init__(self, name=None, path=None):
        self.__name = name
        self.__path = path
        self.__directory = ""
        self.__size = ""
        self.__length = 0
        self.__lastReadWriteTime = time.localtime()  # TODO: I don't curently think so. Do something better

    @property
    def NoteName(self):
        return self.__name

    @NoteName.setter
    def NoteName(self, newName: str):
        self.__name = newName

    @property
    def NotePath(self):
        return self.__path

    @NotePath.setter
    def NotePath(self, newPath: str):
        if (os.path.isfile(newPath)):
            self.__path = newPath

    @property
    def NoteDirectory(self):
        return self.__directory

    @NoteDirectory.setter
    def NoteDirectory(self, newDirectory: str):
        if (os.path.isdir(newDirectory)):
            self.__directory = newDirectory
        raise ValueError

    @property
    def NoteSize(self):
         return  self.__size

    @property
    def NoteLength(self):
         return  self.__length

    @property
    def NoteLastReadWriteTime(self):
         return self.__lastReadWriteTime