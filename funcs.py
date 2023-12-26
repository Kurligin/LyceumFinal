import os
import shutil


class WorkWithDir:
    def __init__(self):
        self._path = os.getcwd()
        self._BookPath = None

        self.CreateBookFolder()

    def CreateBookFolder(self):
        self._BookPath = os.path.join(self._path, 'Books')
        if not os.path.exists(self._BookPath):
            os.mkdir(self._BookPath)

    def MoveBook(self, path):
        name = path.split('/')[-1]
        shutil.copyfile(path, os.path.join(self._BookPath, name))
        return os.path.join('Books', name)

    def RemoveBook(self, path):
        os.remove(path[0])

    def GetPath(self):
        return self._path
