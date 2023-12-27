from PyQt5.QtCore import QUrl

from Database.Database import Database
from Database.Directory import WorkWithDir

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow

import logging

logging.basicConfig(format='%(asctime)s\t|\t%(levelname)s\t|\t%(filename)s\t|\t%(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


class ReaderWindow(QMainWindow):
    def __init__(self, book):
        super().__init__()
        self.Window = QWebEngineView(self)
        self.Window.setWindowTitle('Book')
        self.Window.resize(640, 640)

        self.DB = Database()
        self.DirModule = WorkWithDir()

        self.CurrentChoice = book

        self.LoadBook()

        logging.info('__init__ loaded')

    def LoadBook(self):
        name, author = self.CurrentChoice.text().split(' | ')
        path = self.DB.LoadBook(name, author)

        path = self.DirModule.UnzipFolder(path)

        url = QUrl.fromLocalFile(f'/{path}')
        self.Window.load(url)
        self.setCentralWidget(self.Window)
