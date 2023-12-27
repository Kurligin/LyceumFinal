import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.CreateTable()

    def CreateTable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "books" (
                                "id"	INTEGER NOT NULL UNIQUE,
                                "name"	TEXT NOT NULL UNIQUE,
                                "author"	TEXT NOT NULL,
                                "path"	TEXT NOT NULL,
                                PRIMARY KEY("id" AUTOINCREMENT)
                            )""")
        self.connection.commit()

    def AddBook(self, name, author, path):
        self.cursor.execute(
            "INSERT INTO books VALUES (NULL, ?, ?, ?)",
            (name, author, path)
        )
        self.connection.commit()

    def LoadBook(self, book, author):
        res = self.cursor.execute(
            'SELECT path FROM books WHERE name = ? AND author = ?;',
            (book, author)
        ).fetchall()[0][0]
        return res

    def UpdateBookInfo(self):
        res = self.cursor.execute("SELECT * FROM books").fetchall()
        head = [{'id': i[0], 'name': i[1], 'author': i[2], 'path': i[3]} for i in res]
        return head

    def RemoveBook(self, name):
        res = self.cursor.execute('SELECT path FROM books WHERE name = ?;', [name]).fetchall()[0]
        self.cursor.execute('DELETE FROM books WHERE name = ?;', [name])
        self.connection.commit()
        return res

    def SearchForBook(self, req):
        res = self.cursor.execute(
            "SELECT * FROM books WHERE name LIKE ? OR author LIKE ?;",
            (f'%{req}%', f'%{req}%')
        ).fetchall()
        head = [{'id': i[0], 'name': i[1], 'author': i[2], 'path': i[3]} for i in res]
        return head
