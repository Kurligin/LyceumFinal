from Database.Database import Database
from Database.Directory import WorkWithDir

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

import logging
import os

logging.basicConfig(format='%(asctime)s\t|\t%(levelname)s\t|\t%(filename)s\t|\t%(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)


class SaveWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/SaveWindow.ui', self)

        self.DirModule = WorkWithDir()
        self.DB = Database()
        self.tempPath = None
        self.contPath = None
        self.book = None

        self.FilesButton.clicked.connect(self.SearchFilesButton)
        self.CancelButton.clicked.connect(self.CancelButtonFunc)
        self.SaveButton.clicked.connect(self.SaveButtonFunc)

        logging.info('__init__ loaded')

    def SearchFilesButton(self):
        stuff = (QFileDialog(), 'Select your book', self.DirModule.GetPath(), 'All Files (*)')
        self.tempPath, ext = QFileDialog.getOpenFileName(*stuff)

        if self.tempPath != ' ' and self.tempPath != '':
            self.contPath = self.DirModule.MoveBook(self.tempPath)

            logging.info('File added')
        else:
            self.tempPath = None
            self.contPath = None
            self.book = None
            logging.info('No files')

    def CancelButtonFunc(self):
        if self.contPath:
            os.remove(self.contPath)

        logging.info('Cancel')

        self.NameLine.clear()
        self.AuthorLine.clear()
        self.close()

    def SaveButtonFunc(self):
        name = self.NameLine.text()
        author = self.AuthorLine.text()

        rep = self.DB.cursor.execute(
            'SELECT * FROM books WHERE name = ? AND author = ?',
            (name, author)
        ).fetchall()

        if name == '' or author == '' or self.tempPath is None:
            logging.info('Empty fields')
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("All fields must be complete!\nAlso you need to select book")
            dlg.exec()
        elif rep:
            logging.info('Name | Author repeats')
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Name and Author Repeats")
            dlg.exec()
        else:
            self.DB.AddBook(name, author, self.contPath)
            print(self.contPath)
            self.tempPath = None
            self.contPath = None

            logging.info('Book added')

            self.NameLine.clear()
            self.AuthorLine.clear()
            self.close()
