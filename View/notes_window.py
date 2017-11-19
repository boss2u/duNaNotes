# This is duNaNotes - a notes taking app
# Author - duNaMis
# Date   - 5/5/2016
# Time   - 22:27 PM
# This is the layout file

import logging
import os
import sys

import qdarkstyle
from PyQt4.QtCore import *  # TODO: insert necessary import statement and remove the *:pyqtsignal
from PyQt4.QtGui import (QTabWidget, QMainWindow, QAction, QIcon, QStatusBar, QToolBar, QPixmap,
                                QFont, QLabel, QFontComboBox, QSpinBox, QKeySequence, QMessageBox, QPushButton,
                               QDockWidget, QTextEdit, QTextCursor, QListWidget, QKeyEvent, QApplication)

import MITM.Mediator
import View.TabbedPage
from CustomExceptions import NoNoteException
from Model.Note import Note  # TODO: debugging information, to be removed ASAP
from View.Dialogs.RenameFileDialog import RenameDialog
from View.Dialogs import FindDialog
from View.Dialogs.HelpAboutDialog import HelpAboutDialog
from View.Dialogs.HelpHelpDialog import HelpHelpDialog


##########################################################################################
###Create a QTabWidget
###Create a QWidget for each QTabWidget page
###Populate QWidget with child widget and lay it out
###Put the QWidget into the QTabWidget
##########################################################################################


class NotesMainWindow(QMainWindow):
    """The view class"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Load saved application settings
        self.recentNotes = []

        self.numberOfTabs = 0  # keep track of the total number of tabs in the window
        self.currentPage = None
        self.__mediator = MITM.Mediator.Mediator()  # the mediator object. intermediary btwn view and model

        # create a timer
        timer = QTimer(self)
        # dialogs: saved to avoid eating memory by constant cre- and re- creation
        self.findDialog = None
        self.renameDialog = None
        self.helpAboutDialog = HelpAboutDialog(self)
        self.helpHelpDialog = HelpHelpDialog(self)
        self.recentFilesListWidget = QListWidget

        # create menus first
        self.fileMenu = self.menuBar().addMenu("File")
        self.recentNotesMenu = self.fileMenu.addMenu("Open Recent")
        self.editMenu = self.menuBar().addMenu("Edit")
        self.syncMenu = self.menuBar().addMenu("Sync")
        self.helpMenu = self.menuBar().addMenu("Help")

        # region Actions
        # create the menu actions
        # first the file menu actions
        fileNewAct = self.createAction(self, "&New", shortcut=QKeySequence.New,
                                       tooltip="Create a new note", enabled=True, slot=self.onNewClick)
        fileOpenRecentNotesAct = self.createAction(self, "&Open Recent Note",
                                        tooltip="open recent notes", enabled=True, slot=self.onOpenRecentNotes)
        fileQuitAct = self.createAction(self, "&Exit", shortcut=QKeySequence.Quit,
                                        tooltip="Exit the application", enabled=True, slot=self.close)

        # recent files menu actions
        self.recentFilesMenuAct = self.createAction(self.recentNotesMenu, "File 1")

        # edit menu actions
        editInsertAct = self.createAction(self, "Ins&ert...", shortcut="Ctrl+I",
                                        tooltip="Insert a media file", enabled=True)
        editPreferencesAct = self.createAction(self, "&Preferences", shortcut="Ctrl+Shift+P",
                                        tooltip="Set application preferences", enabled=True)
        editFindAct = self.createAction(self, "&Find", shortcut=QKeySequence.Find,
                                        tooltip="Find a text string", slot=self.onFind)
        editUndoAct = self.createAction(self, "&Undo", shortcut=QKeySequence.Undo,
                                        tooltip="Roll back changes to document", slot=self.onUndo)
        editRedoAct = self.createAction(self, "&Redo", shortcut=QKeySequence.Redo,
                                        tooltip="Repeat the last action", slot=self.onRedo)
        editRenameAct = self.createAction(self, "&Rename...", shortcut="Ctrl+Shift+R",
                                        tooltip="Rename current note", slot=self.onRenameNote)

        # sync menu actions
        synCloudAcctAct = self.createAction(self, "Cloud &Account", shortcut="Alt+A",
                                        tooltip="Sync with cloud accounts", enabled=True)

        # help menu actions
        helpHelpAct = self.createAction(self, "Help", shortcut=QKeySequence.HelpContents,
                                        tooltip="Display help", enabled=True, slot=self.onHelpHelp)
        helpAboutAct = self.createAction(self, "A&bout", shortcut="Ctrl+Shift+B",
                                        tooltip="About application", enabled=True, slot=self.onHelpAbout)

        boldTextAction = self.createAction(self, "B", shortcut="Ctrl+B", tooltip="Bold text")
        italicsTextAction = self.createAction(self, "<i>I</i>", shortcut="Ctrl+I", tooltip="Italics text")
        # endregion

        # add actions to corresponding menu
        self.addActions_(self.fileMenu, (fileNewAct, fileOpenRecentNotesAct, fileQuitAct))  # to file menu
        self.addActions_(self.editMenu,
                         (editRenameAct, editUndoAct, editRedoAct, editFindAct, editInsertAct, editPreferencesAct))  # to edit menu
        self.addActions_(self.helpMenu, (helpHelpAct, helpAboutAct))  # to help menu
        self.addActions_(self.recentNotesMenu, (self.recentFilesMenuAct,))
        # create tool bar and add relevant actions
        allToolBar = self.addToolBar("All Tools")  # tool bar that contains all tool;not separated into file/edit/*
        self.addActions_(allToolBar,
                         (fileNewAct, synCloudAcctAct, editInsertAct, editFindAct, editUndoAct, editRedoAct))

        fontDetailsToolBar = self.addToolBar("Font Details")
        self.fontTypeComboBox = QFontComboBox(fontDetailsToolBar)  # get font list present on the user system
        self.fontSizeSpinBox = QSpinBox(fontDetailsToolBar)  # size of the font
        self.fontSizeSpinBox.setMinimum(7)
        self.fontSizeSpinBox.setValue(12)
        self.textBoldButton = QPushButton("B")
        self.addNewNoteButton = QPushButton("+")
        self.textItalicsButton = QPushButton("I")
        maskLabel = QLabel(fontDetailsToolBar)  # TODO: experimental, to be removed
        pixmap = QPixmap("Asset/guit.png")  # TODO: experimental, remove
        maskLabel.setPixmap(pixmap.mask())  # TODO: experimental, remove
        self.addWidgetToToolBar(fontDetailsToolBar,
                        (self.fontTypeComboBox, self.fontSizeSpinBox, self.textBoldButton, self.textItalicsButton))
        # self.addActions_(fontDetailsToolBar, (boldTextAction, italicsTextAction))


        # create a QTabWidget
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabPosition(QTabWidget.South)
        # self.setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.South)  # TODO: not working yet. Handled
        self.tabWidgetTabBar = self.tabWidget.tabBar()
        self.tabWidget.setCornerWidget( self.addNewNoteButton, Qt.TopRightCorner)

        # create pages  # TODO:     let an event handler handle this job: HANDLED
        self.onWindowStartOpenNote()
        # self.page1 = View.TabbedPage.TabbedPage(self, Note("First", "/path"))
        # # add the pages to the tab Widget
        # self.tabWidget.addTab(self.page1, "Note 1 ")
        # self.currentPage = self.tabWidget.currentWidget()
        self.setCurrentPage()
        #        print("count() returned: ", self.tabWidget.count())

        # create "+" bar:  TODO: find a better way to create a plus tab: DONE
        # self.plusTabIndex = self.tabWidgetTabBar.insertTab(self.tabWidget.count() + 1,
        #                                         "+")  # this tab bears the "+" sign that indicates 'create new tab'
        # self.plusTabWidget = self.tabWidget.widget(self.plusTabIndex)  # get a reference to the plus tab widget

        # create Dock widget that holds find dialog
        # self.dockWidget = QDockWidget(self)
        # self.dockWidget.setAllowedAreas(Qt.TopDockWidgetArea)
        # self.dockWidget.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetMovable)
        # self.dockWidget.setWidget(FindDialog.FindDialog(self.currentPage, self))
        # self.dockWidget.hide()

        # do window namings and other stuffs
        self.statusbar = QStatusBar(self)
        self.statusbar.setSizeGripEnabled(False)
        self.setStatusBar(self.statusbar)
        self.setCentralWidget(self.tabWidget)
        self.setWindowTitle("Notes")

        # region Signal And Slot Bindings
        self.tabWidget.currentChanged.connect(self.setCurrentPage)
        # self.currentPage.firstTime.connect(self.openPageOnFirstNavigation)
        self.tabWidget.currentChanged.connect(self.notifyMediatorOfCurrentPageChange)
        # fileNewAct.triggered.connect(self.onNewClick)
        # fileQuitAct.triggered.connect(self.close)
        self.tabWidget.tabCloseRequested.connect(self.confirmTabCloseAndCloseTab)
        # self.tabWidget.tabCloseRequested.connect(self.holla)
        self.fontTypeComboBox.currentFontChanged.connect(self.changeFont)
        self.fontSizeSpinBox.valueChanged.connect(self.changeFontSize)
        self.textBoldButton.clicked.connect(self.toggleTextBold)
        self.textItalicsButton.clicked.connect(self.toggleTextItalics)
        timer.timeout.connect(self.onSaveClick)
        timer.timeout.connect(self.timed)
        self.addNewNoteButton.clicked.connect(self.onNewClick)
        self.currentPage.cursorPositionChanged.connect(self.reportCurrentCursor)
        self.recentNotesMenu.aboutToShow.connect(self.updateRecentNotesMenu)
        # editUndoAct.triggered.connect(self.currentPage.undo)
        # editRedoAct.triggered.connect(self.currentPage.redo)
        # endregion

        self.readSettings()
        # QTimer.singleShot(5000, self.onSaveClick)
        # Start the timer
        timer.start(1500000)
        # Application settings

    # region Methods
    def updateRecentNotesMenu(self):
        """Repopulate the recent files menu"""
        self.recentNotesMenu.clear()
        for note in self.recentNotes:
            if os.path.exists(self.mediator.returnNotePath(note)):
                noteName, ext = os.path.basename(note).split(".")
                act = self.createAction(self.recentNotesMenu, noteName, slot=self.loadNotes)  #TODO: incomplete update loadNotes() to receive the noteName
                self.addActions_(self.recentNotesMenu, (act,))

    def onOpenRecentNotes(self):
        """"""

    def reportCurrentCursor(self):
        print("###### cursor position has changed now #####")  # TODO: remove
        print("current font is: ", self.currentPage.currentFont().family())
        self.fontTypeComboBox.setCurrentFont(self.currentPage.currentFont())
        self.fontSizeSpinBox.setValue(self.currentPage.currentFont().pointSize())

    def onRecentNotes(self):
        self.recentFilesListWidget.show()

    def toggleTextItalics(self):
        self.currentPage.setFontItalic(not self.currentPage.fontItalic())
        self.currentPage.setFocus()
        # if not self.textItalicsButton.isChecked():
        #     self.textItalicsButton.setChecked(True)
        #     self.currentPage.setFontItalic(True)
        #     self.currentPage.setFocus()
        #     return
        # self.textItalicsButton.setChecked(False)
        # self.currentPage.setFontItalic(False)
        # self.currentPage.setFontItalic(checked)
        # self.currentPage.setFontItalic(not self.currentPage.fontItalic)

    def keyPressEvent(self, event:QKeyEvent):
        if event.modifiers() and Qt.ControlModifier:
            handled = False
        if event.key() == Qt.Key_B:
            self.toggleTextBold()  # bolden text
            handled = True
        elif event.key() == Qt.Key_I:
            self.toggleTextItalics()  # italicise text
            handled = True
            print("Ctrl+I")

        if handled:
            event.accept()
            return
        else:
            QTextEdit.keyPressEvent(self.currentPage, event)

    def toggleTextBold(self):
        self.currentPage.setFontWeight(QFont.Normal
                if self.currentPage.fontWeight() > QFont.Normal else QFont.Bold)
        # if not self.textBoldButton.isChecked():
        #     # self.textBoldButton.setChecked(True)
        #     self.currentPage.setFontWeight(QFont.Bold)
        #     self.currentPage.setFocus()
        #     return
        # # self.textBoldButton.setChecked(False)
        # self.currentPage.setFontWeight(QFont.Normal)
        self.currentPage.setFocus()
        # self.currentPage.setFontWeight(QFont.Bold) if checked else \
        #                                     self.currentPage.setFontWeight(QFont.Normal)
        # self.currentPage.setFocus()

    def changeFontSize(self, value:float):
        self.currentPage.setFontPointSize(value)
        self.currentPage.setFocus()

    def changeFont(self, font:QFont):
        self.currentPage.setCurrentFont(font)
        self.currentPage.setFocus()

    def addWidgetToToolBar(self, toolBar:QToolBar, widgets:tuple):
        for widget in widgets:
            toolBar.addWidget(widget)

    def holla(self, index):
        """Debugging Method. To be removed in release code"""
        print("<<<<**** Hey! holla! Removing: .... ", index)

    def timed(self):
        """Debugging Method. To be removed in release code"""
        print("\n$$$$> Called by timer")
    # region Methods

    def onWindowStartOpenNote(self):
        for note_file in self.findNotesInCurrentDirectory(applicationDirectory):  # find all the notes in the app dir
            self.createNoteObjectFromNoteFile(note_file)  # create note objs from the files
        self.createAndLoadNotes()

    def createNoteObjectFromNoteFile(self, note_file:str):
        self.mediator.createNote(notePath=note_file)

    def createAndLoadNotes(self):  # Trent Harmon: When a man loves a woman....song request
        if len(self.mediator.notesCollection) > 0:
            self.loadNotes()
        else:  # couldn't find a note obj
            self.createOnlyOneNote()

    def loadNotes(self):
        """Creates a TabbedPage for each note found in notes collection
            Without reading the contents of the associated note file found
            In note path"""
        note = self.sender().getData() if self.sender() is QAction else None
        if note:
            pageIndex = self.createNotePage(note)
            self.tabWidget.setCurrentIndex(pageIndex)


        for note in self.mediator.NotesCollection:
            self.createNotePage(note)
            # self.mediator.setCurrentlyDisplayedNote(note)

    def createNotePage(self, note):
        page = View.TabbedPage.TabbedPage(self, note)
        pageIndex = self.tabWidget.addTab(page, note.NoteName)
        page.page_number = pageIndex
        return pageIndex

    def createOnlyOneNote(self):
        page1 = View.TabbedPage.TabbedPage(self, Note("First", "/path"))
        # add the pages to the tab Widget
        self.tabWidget.addTab(page1, "Note 1 ")

    def openPageOnFirstNavigation(self):
        """Reads the content of the file on first nav.
            Implements something like lazy loading
            Implementation is whack. 
            Implementation Path:
                onWindowStart -> createNoteObjectFromNoteFile -> createAndLoadNotes ->
                loadNotes -> openPageOnFirstNavigation
            TODO: make a better lazy loading implementatiion"""
        # TODO: make a better lazy loading implementatiion
        print("\n<<<<<I also work\n")
        self.mediator.setCurrentlyDisplayedNote(self.currentPage.getNote())
        try:
            contents = self.mediator.openCurrentNote()
            self.currentPage.setHtml(contents)
            self.currentPage.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)  # move the cursor to the end of the document
            self.currentPageIsNowDirty(False)
        except IOError as e:
            logging.error("Note is not on filesystem yet: {}".format(e))

    def currentPageIsNowDirty(self, bool_:bool=False):
        self.currentPage.dirty = False

    @property
    def mediator(self):
        return self.__mediator

    @mediator.setter
    def mediator(self, newMediator):
        if isinstance(newMediator, MITM.Mediator.Mediator):
            self.__mediator = newMediator
        else:
            raise TypeError("newMediator must be of type Mediator")

    def writeSettings(self) -> None:
        settings = QSettings()
        settings.setValue("mainWindow/pos", self.pos())
        settings.setValue("mainWindow/size", self.size())
        settings.setValue("mainWindow/state", self.windowState())
        openedNotes = [note.NotePath for note in self.mediator.NotesCollection]
        settings.setValue("list of opened notes", openedNotes)
        fontAttrList = self.fontTypeComboBox.currentFont().toString(); print("/////////>>>>  ", fontAttrList)
        settings.setValue("mainWindow/font", fontAttrList)
        settings.setValue("mainWindow/fontSize", self.fontSizeSpinBox.value())

    def readSettings(self):
        settings = QSettings()
        self.resize(settings.value("mainWindow/size", QSize(800, 600)))
        pos = settings.value("mainWindow/pos", QPoint(0, 0))
        listOfOpenedNotes = settings.value("list of opened notes")
        print("Opened notes:", listOfOpenedNotes)
        fontDetails = settings.value("mainWindow/font", "Architext, -1, -1, False")
        fontSize = settings.value("mainWindow/fontSize", 12)
        family, _, _, fontWeight, italics,* _ = fontDetails.split(",")
        font = QFont(family, int(fontSize), int(fontWeight), bool(italics))
        self.fontTypeComboBox.setCurrentFont(font)
        self.fontSizeSpinBox.setValue(int(fontSize))
        self.textItalicsButton.click() if font.italic() else self.textItalicsButton.clearFocus()  #TODO: code smell, review later
        self.textBoldButton.click() if font.bold() else self.textBoldButton.clearFocus()  #TODO: code smell, review later
        self.move(pos)
        self.restoreState(settings.value("mainWindow/state"))

    def setCurrentPage(self):
        """Updates the self.currentPage variable"""
        self.currentPage = self.tabWidget.currentWidget()
        self.currentPage.I_becameCurrentPage()
        print(":::::::::  New current page set: ", self.currentPage.getNote().NoteName)  # TODO: remove

    def notifyMediatorOfCurrentPageChange(self):
        self.mediator.setCurrentlyDisplayedNote(self.currentPage.getNote())

    def onNewClick(self):
        """Create a new area to write new note"""
        tabCount = self.tabWidget.count() + 1
        noteObject = self.mediator.createNote(tabCount)
        page = View.TabbedPage.TabbedPage(self, note=noteObject)
        newPageIndex = self.tabWidget.addTab(page, "Note {}".format(tabCount))  # add the page to the parent tabWidget
        page.page_number = newPageIndex  # assign a number to the page
        self.numberOfTabs = self.tabWidget.count()
        # self.tabWidgetTabBar.moveTab(self.plusTabIndex,
        #             self.numberOfTabs)  # move the "+" tab to the end TODO: update the index of the plus tab widget
        self.moveToTab(newPageIndex)
        self.currentPage.setFocus()


    def moveToTab(self, newPageIndex:int):
        self.tabWidgetTabBar.setCurrentIndex(newPageIndex)  # switch to the just created page

    def onSaveClick(self, pages:list=[]):
        """This method gets the text from the current page;
                Passes the text along with the attached Note object to the mediator to save
        """
        if len(pages) == 0:  # pages is a list of note pages to be saved
            pages.append(self.currentPage)

        for page in pages:
            if page.dirty:
                rich_text = page.toHtml()  # get the text from the current document
                # note = self.currentPage.getNote()  # get the Note object attached to this page
                try:
                    self.mediator.saveNote(rich_text, page.getNote())  # give the text document to the mediator
                    self.currentPageIsNowDirty(False)
                except IOError as error:
                    QMessageBox(self, "File Save Error", "Could not save the file", "Ok")
                    assert isinstance(error, IOError)  # pycharm suggested this, I don't think it's needed here
                    print("Error", "IOError occurred", error)
                    logging.log(1, "IOError occurred", error)
                except NoNoteException as error:
                    # QMessageBox.critical(self, "File Save Error", "Could not save the file: {}".format(error),
                    #             "Ok")  # TODO:Not sure this will work yet. Handled
                    print("Error", "IOError occurred: No Note", error)
                    logging.log(1, error)
            else:
                print("\n-----> No changes made to code")

    def onRenameNote(self):
        """Rename a Note"""
        # TODO : create a rename dialog window later
        renameDialog = RenameDialog(self)
        if renameDialog.exec_():
            newName = renameDialog.getNewName()
            try:
                self.mediator.renameNote(newName)
                self.tabWidget.setTabText(self.currentPage.page_number, newName)
            except Exception as e:  # TODO: what error exactly
                print("Error renaming this file:   ", e)  # TODO: do better, inform  the user of the problem
                raise e

    def onUndo(self):
        """Connect to QTextEdit undo slot. A work around for inability to connect a QAction to
           QTextEdit undo slot.
        """
        self.currentPage.undo()

    def onRedo(self):
        """Connect to QTextEdit undo slot. A work around for inability to connect a QAction to
            QTextEdit undo slot.
         """
        self.currentPage.redo()
        # cus = CustomSignal()
        # cus.redoTriggered.connect(QTextEdit.redo)

    def onFind(self):  # TODO: song request Paul I.K. Dairo: Mo wa dupe
        textSelected = self.currentPage.getDocumentCursor().selectedText()
        print("Text Selected is:  ", textSelected)
        self.findDialog = FindDialog.FindDialog(self.currentPage, self, textSelected)
        self.findDialog.show()
        # self.dockWidget.show()

    def onHelpAbout(self):
        self.helpAboutDialog.show()

    def onHelpHelp(self):
        self.helpHelpDialog.show()

    def closeEvent(self, event: QEvent):
        # TODO: raise a dialog that prompts the user to accept the closing of the application
        """
        :type event: QEvent
        """
        numberOfPages = self.tabWidget.count()
        widgetList = [self.tabWidget.widget(widget) for widget in range(numberOfPages)]
        # self.onSaveClick(widgetList)  # save notes first
        self.writeSettings()
        event.accept()

    def confirmTabCloseAndCloseTab(self, index):
        pageToRemove = self.tabWidget.widget(index)
        if pageToRemove.dirty and isinstance(pageToRemove, View.TabbedPage.TabbedPage):
            print("Tab Close requested")
            dialog = QMessageBox.warning(self, "Confirm","Do you want to close the tab?", "Ok", "Cancel", "", 1)
            if dialog != 0:
                return
        self.tabWidget.removeTab(pageToRemove.page_number)
        self.recentNotes.append(pageToRemove.getNote())

    @staticmethod
    def addActions_(parent, actions: tuple) -> None:
        for action in actions:
            parent.addAction(action)

    @staticmethod
    def createAction(parent: QObject, text: str, icon: object = None, shortcut: str = None, tooltip: str = None,
                     enabled: bool = False, signal: str = "triggered", slot: object = None) -> object:
        action = QAction(parent)
        action.setText(text)
        if icon:
            action.setIcon(QIcon(icon))  # icon is expected as a string argument
        if shortcut:
            action.setShortcut(shortcut)
        if tooltip:
            action.setToolTip(tooltip)
        if enabled:
            action.setEnabled(enabled)

        if slot and signal == "triggered":
            action.pyqtConfigure(triggered=slot)

        return action

    @staticmethod
    def findNotesInCurrentDirectory(directory: str):
        if os.path.exists(directory):
            for path, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".dn"):
                        fullPath = os.path.join(directory, path, file)
                        yield os.path.normpath(os.path.abspath(fullPath))

    def __str__(self):
        print("I am a note window with id {}".format(self.winId()))

    def __repr__(self):
        print(r"I am a note")

    #endregion


class CustomSignal(QObject):
    redoTriggered = pyqtSignal(name="redoTriggered")
    undoTriggered = pyqtSignal(name="undoTriggered")  # signal to indicate that an undo operation is needed.

    def __init__(self, parent=None):
        super(CustomSignal, self).__init__(parent)
        # self.redoTriggered.emit()

    def redoPressed(self):
        print("CALLED")
        self.redoTriggered.emit()


# class CustomTabWidget(QTabWidget):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
    # def


def on_current_widget_changed():
    logging.info("Current widget is now: ", notes.tabWidget.currentWidget())


if __name__ == '__main__':
    try:  # TODO: move this try/except block into the onStart event handler for the application
        homeFolder = os.environ["HOME"]
        if not os.path.exists(homeFolder + "/.Notes/"):
            os.mkdir(homeFolder + "/.Notes")  # create the application directory
            applicationDirectory = homeFolder + "/.Notes"  # set application directory
    except IOError as e:
        print("Error occurred, exiting application", e)
        os._exit(1)

    finally:
        applicationDirectory = homeFolder + "/.Notes"  # set application directory

    app = QApplication(sys.argv)
    app.setStyleSheet(
        qdarkstyle.load_stylesheet(pyside=False))  # TODO: create my own style sheet probably using this as template
    notes = NotesMainWindow()
    # print(notes.page1.page_number)
    # print(notes.page2.page_number)
    # print(notes.page3.page_number)

    # print("I am notebookrename number : ", notes.page3.getCurrentPageNumber())
    # print("I am notebook number : ", notes.page1.getCurrentPageNumber())
    # print("I am notebook number : ", notes.page2.getCurrentPageNumber())
    # notes.page1.setDocumentTitle("Note User Set")
    # print("Note1 document title is: ", notes.page1.documentTitle())
    notes.tabWidget.currentChanged.connect(on_current_widget_changed)

    notes.show()
    app.exec_()





