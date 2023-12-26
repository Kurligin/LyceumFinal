from Database.Database import Database
from funcs import WorkWithDir

from Windows.BookAddWindow import SaveWindow

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import logging
import webbrowser

logging.basicConfig(format='%(asctime)s\t|\t%(levelname)s\t|\t%(filename)s\t|\t%(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/StartWindow.ui', self)

        self.DirModule = WorkWithDir()
        self.DB = Database()

        self.CurrentChoice = None
        self.SearchWindow = None

        self.SearchLine.setPlaceholderText('Enter your book name')

        self.NewButton.clicked.connect(self.NewBookButton)
        self.OpenButton.clicked.connect(self.OpenBookButton)
        self.SearchButton.clicked.connect(self.SearchBookButton)
        self.DeleteButton.clicked.connect(self.DeleteBookButton)
        self.BooksButton.clicked.connect(self.FindBookButton)

        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QListWidgetItem.html
        self.ListWidget.itemPressed.connect(self.BookChoiceList)

        books = self.DB.UpdateBookInfo()
        self.ListWidget.addItems([f'{i["name"]} | {i["author"]}' for i in books])

        logging.info('__init__ loaded')

    def NewBookButton(self):
        if self.SearchWindow is None:
            self.SearchWindow = SaveWindow()
        self.SearchWindow.show()
        logging.info('Created new book')

        self.ListWidget.clear()
        self.ListWidget.addItems(['Press to update'])

    def OpenBookButton(self):
        logging.info('Opened book')

    def SearchBookButton(self):
        text = self.SearchLine.text()

        if text != '' and text != '':
            books = self.DB.SearchForBook(text)
            self.ListWidget.clear()
            self.ListWidget.addItems([f'{i["name"]} | {i["author"]}' for i in books])
        logging.info('Searched for books')

    def DeleteBookButton(self):
        if self.CurrentChoice is not None:
            dlg = QMessageBox(self)
            dlg.setText("You want to remove book?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                self.ListWidget.takeItem(self.ListWidget.row(self.CurrentChoice))
                path = self.DB.RemoveBook(self.CurrentChoice.text().split(' | ')[0])
                self.DirModule.RemoveBook(path)

                logging.info(f'Book {self.CurrentChoice.text()} was removed')
            else:
                logging.info(f'Book was not removed')

    def FindBookButton(self):
        webbrowser.open('https://gutenberg.org/')

    def BookChoiceList(self, i):
        self.CurrentChoice = i
        logging.info(f'{i.text()} Was selected')

        if i.text() == 'Press to update':
            self.ListWidget.clear()
            books = self.DB.UpdateBookInfo()
            self.ListWidget.addItems([f'{i["name"]} | {i["author"]}' for i in books])
