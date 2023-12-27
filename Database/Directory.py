import fnmatch
import os
import shutil
import zipfile


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

    def UnzipFolder(self, path):
        with zipfile.ZipFile(path, 'r') as folder:
            newFolder = os.path.join('Books', path.split('/')[-1].split('.zip')[0])
            folder.extractall(path=newFolder)
            folder.close()

        result = str()
        for root, dirs, files in os.walk(newFolder):
            for name in files:
                if fnmatch.fnmatch(name, '*.html'):
                    result = os.path.join(root, name)

        return result
