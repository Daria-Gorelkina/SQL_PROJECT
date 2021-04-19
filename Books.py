import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QTableWidgetItem, QInputDialog, QMessageBox


class MyWidget2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ADDBOOK.ui', self)


class MyWidget3(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FINDBOOK.ui', self)


class MyWidget4(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UPDATEBOOK.ui', self)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.n = None
        self.New_Window = None
        self.newWindow2 = None
        self.newWindow = None
        self.author = None
        self.st = None
        self.genre = None
        self.name = None
        self.id = None
        self.NB = None
        self.AB = None
        self.status = 0
        self.modified = {}
        self.ids = None
        uic.loadUi('Books_QT.ui', self)
        self.titles = None
        self.tabWidget.setTabText(0, 'Книги')
        self.tabWidget.setTabText(1, 'Жанры')
        self.tabWidget.setTabText(2, 'Авторы')
        self.connection = sqlite3.connect("BOOKS.db")
        self.opinions = ''
        self.initQT()
        self.add_readbook.clicked.connect(self.addReadBook)
        self.delete_readbook.clicked.connect(self.delete_elem)
        self.tableWidget.itemClicked.connect(self.elem_clicked)
        self.TableGenres.itemClicked.connect(self.Item_clicked)
        self.TableAuthors.itemClicked.connect(self.ItemClickedA)
        self.update_readbook.clicked.connect(self.updateBook)
        self.findreadbook.clicked.connect(self.findbook)
        self.Add_genre.clicked.connect(self.addgenre)
        self.Delete_genre.clicked.connect(self.deleteGenre)
        self.Add_author.clicked.connect(self.addauthor)
        self.Delete_author.clicked.connect(self.deleteauthor)
        self.Update_genre.clicked.connect(self.SaveResultsForGenre)
        self.Update_author.clicked.connect(self.SaveResultsForAuthors)

    def initQT(self):
        books = self.connection.cursor().execute("SELECT * FROM "
                                                 "Read").fetchall()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(books):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.FromNumToName()
        authors = self.connection.cursor().execute("SELECT * FROM aut"
                                                   "hors").fetchall()
        self.TableAuthors.setColumnCount(2)
        self.TableAuthors.setRowCount(0)
        for i, row in enumerate(authors):
            self.TableAuthors.setRowCount(
                self.TableAuthors.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableAuthors.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        genres = self.connection.cursor().execute("SELECT * FROM "
                                                  "genres").fetchall()
        self.TableGenres.setColumnCount(2)
        self.TableGenres.setRowCount(0)
        for i, row in enumerate(genres):
            self.TableGenres.setRowCount(
                self.TableGenres.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableGenres.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def addReadBook(self):
        self.newWindow = MyWidget2()
        self.newWindow.status.addItems(['Да', 'Нет'])
        self.newWindow.show()
        self.customizationWindow()
        self.newWindow.pushButton.clicked.connect(self.add)

    def customizationWindow(self):
        genres = self.connection.cursor().execute("SELECT genre FROM "
                                                  "genres").fetchall()
        for elem in genres:
            self.newWindow.genre.addItem(str(elem[0]))
        self.newWindow.genre.setEditable(True)
        authors = self.connection.cursor().execute(
            "SELECT author FROM authors").fetchall()
        for elem in authors:
            self.newWindow.author.addItem(str(elem[0]))
        self.newWindow.author.setEditable(True)
        years = self.connection.cursor().execute(
            "SELECT year FROM years").fetchall()
        for elem in years:
            self.newWindow.year.addItem(str(elem[0]))
        self.newWindow.year.setEditable(True)

    def add(self):
        name = self.newWindow.name.text()
        number = self.newWindow.number.text()
        genre = self.newWindow.genre.currentText()
        author = self.newWindow.author.currentText()
        year = self.newWindow.year.currentText()
        status = self.newWindow.status.currentText()
        if not name or not number or not genre or not author or \
                not year or not status:
            self.newWindow.statusBar().showMessage('Заполните '
                                                   'все поля!')
        else:
            if status == 'Да':
                self.status = 1
                opinion, ok_pressed = QInputDialog.getText(self,
                                                           "Ваше "
                                                           "впечат"
                                                           "ление",
                                                           "Напишите "
                                                           "свое "
                                                           "мнение о "
                                                           "книге")
                if ok_pressed:
                    self.opinions = opinion
                else:
                    self.opinions = ''
            else:
                self.opinions = ''
                self.status = 0
            ID = self.connection.cursor().execute("SELECT id FROM "
                                                  "authors "
                                                  "WHERE author=?",
                                                  (author,)
                                                  ).fetchall()
            if not ID:
                self.connection.cursor().execute(
                    f"""INSERT INTO authors(author) VALUES(
                     ?)""", (author,))
                self.connection.commit()
                author = self.connection.cursor().execute(
                    "SELECT id FROM authors WHERE author=?",
                    (author,)).fetchall()
            else:
                author = ID
            ID2 = self.connection.cursor().execute("SELECT id FROM "
                                                   "genres "
                                                   "WHERE genre=?",
                                                   (genre,)
                                                   ).fetchall()
            if not ID2:
                self.connection.cursor().execute(
                    f'INSERT INTO genres(genre) VALUES({genre})')
                self.connection.commit()
                genre = self.connection.cursor().execute(
                    "SELECT id FROM genres WHERE genre=?",
                    (genre,)).fetchall()
            else:
                genre = ID2
            ID3 = self.connection.cursor().execute("SELECT id FROM "
                                                   "years "
                                                   "WHERE year=?",
                                                   (year,)).fetchall()
            if not ID3:
                self.connection.cursor().execute(
                    f'INSERT INTO years(year) VALUES({year})')
                self.connection.commit()
                year = self.connection.cursor().execute(
                    "SELECT id FROM years WHERE year=?",
                    (year,)).fetchall()
            else:
                year = ID3
            self.connection.cursor().execute(f"INSERT INTO Read("
                                             f"name, author, "
                                             f"number_of_pages, "
                                             f"genre, year, "
                                             f"impression, status) "
                                             f" VALUES (?, ?, ?, ?,"
                                             f" ?, ?, ?)",
                                             (name,
                                              int(author[0][0]),
                                              int(number),
                                              int(genre[0][0]),
                                              int(year[0][0]),
                                              self.opinions,
                                              self.status))
            self.connection.commit()
            books = self.connection.cursor().execute("SELECT * FROM "
                                                     "Read"
                                                     ).fetchall()
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(books):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.FromNumToName()
            self.newWindow.hide()

    def delete_elem(self):
        rows = list(
            set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '',
            "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.connection.cursor()
            cur.execute("DELETE FROM Read WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.connection.commit()

        books = self.connection.cursor().execute("SELECT * FROM "
                                                 "Read"
                                                 ).fetchall()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(books):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def findbook(self):
        self.newWindow2 = MyWidget3()
        self.newWindow2.setWindowTitle('Поиск книг')
        self.newWindow2.comboBox.addItems(['Названию',
                                           'Числу страниц', 'Жанру',
                                           'Статусу', 'Автору'])
        self.newWindow2.show()
        self.newWindow2.pushButton.clicked.connect(self.Find)

    def Find(self):
        if self.newWindow2.lineEdit.text() == '':
            self.newWindow2.statusBar().showMessage('Неправильный '
                                                    'запрос')
        else:
            if self.newWindow2.comboBox.currentText() == 'Названию':
                self.name = self.newWindow2.lineEdit.text()
                res = self.connection.cursor().execute("SELECT * "
                                                       "FROM Read "
                                                       "WHERE "
                                                       "name=?",
                                                       (self.name,)
                                                       ).fetchall()
                if not res:
                    self.newWindow2.statusBar().showMessage(
                        'Ничего не найдено')
                else:
                    self.newWindow2.tableWidget.setColumnCount(8)
                    self.newWindow2.tableWidget.setRowCount(0)
                    for i, row in enumerate(res):
                        self.newWindow2.tableWidget.setRowCount(
                            self.newWindow2.tableWidget.rowCount() + 1
                        )
                        for j, elem in enumerate(row):
                            self.newWindow2.tableWidget.setItem(
                                i, j, QTableWidgetItem(str(elem)))

            if self.newWindow2.comboBox.currentText() == 'Жанру':
                self.genre = self.newWindow2.lineEdit.text()
                res = self.connection.cursor().execute("SELECT * "
                                                       "FROM Read "
                                                       "WHERE "
                                                       "genre=("
                                                       "SELECT id "
                                                       "FROM genres "
                                                       "WHERE genre "
                                                       "= ?)",
                                                       (self.genre,)
                                                       ).fetchall()
                if not res:
                    self.newWindow2.statusBar().showMessage(
                        'Ничего не найдено')
                else:
                    self.newWindow2.tableWidget.setColumnCount(8)
                    self.newWindow2.tableWidget.setRowCount(0)
                    for i, row in enumerate(res):
                        self.newWindow2.tableWidget.setRowCount(
                            self.newWindow2.tableWidget.rowCount() + 1
                        )
                        for j, elem in enumerate(row):
                            self.newWindow2.tableWidget.setItem(
                                i, j, QTableWidgetItem(str(elem)))

            if self.newWindow2.comboBox.currentText() == 'Числу ' \
                                                         'страниц':
                self.n = int(self.newWindow2.lineEdit.text())
                res = self.connection.cursor().execute("SELECT * "
                                                       "FROM Read "
                                                       "WHERE "
                                                       "number_of_pag"
                                                       "es=?",
                                                       (self.n,)
                                                       ).fetchall()
                if not res:
                    self.newWindow2.statusBar().showMessage(
                        'Ничего не найдено')
                else:
                    self.newWindow2.tableWidget.setColumnCount(8)
                    self.newWindow2.tableWidget.setRowCount(0)
                    for i, row in enumerate(res):
                        self.newWindow2.tableWidget.setRowCount(
                            self.newWindow2.tableWidget.rowCount() + 1
                        )
                        for j, elem in enumerate(row):
                            self.newWindow2.tableWidget.setItem(
                                i, j, QTableWidgetItem(str(elem)))

            if self.newWindow2.comboBox.currentText() == 'Автору':
                self.author = self.newWindow2.lineEdit.text()
                res = self.connection.cursor().execute("SELECT * "
                                                       "FROM Read "
                                                       "WHERE "
                                                       "author=("
                                                       "SELECT id "
                                                       "FROM authors "
                                                       "WHERE author "
                                                       "= ?)",
                                                       (self.author,)
                                                       ).fetchall()
                if not res:
                    self.newWindow2.statusBar().showMessage(
                        'Ничего не найдено')
                else:
                    self.newWindow2.tableWidget.setColumnCount(8)
                    self.newWindow2.tableWidget.setRowCount(0)
                    for i, row in enumerate(res):
                        self.newWindow2.tableWidget.setRowCount(
                            self.newWindow2.tableWidget.rowCount() + 1
                        )
                        for j, elem in enumerate(row):
                            self.newWindow2.tableWidget.setItem(
                                i, j, QTableWidgetItem(str(elem)))

            if self.newWindow2.comboBox.currentText() == 'Статусу':
                self.st = self.newWindow2.lineEdit.text()
                res = self.connection.cursor().execute("SELECT * "
                                                       "FROM Read "
                                                       "WHERE "
                                                       "status=("
                                                       "SELECT id "
                                                       "FROM "
                                                       "statuses "
                                                       "WHERE status "
                                                       "= ?)",
                                                       (self.st,)
                                                       ).fetchall()
                if not res:
                    self.newWindow2.statusBar().showMessage(
                        'Ничего не найдено')
                else:
                    self.newWindow2.tableWidget.setColumnCount(8)
                    self.newWindow2.tableWidget.setRowCount(0)
                    for i, row in enumerate(res):
                        self.newWindow2.tableWidget.setRowCount(
                            self.newWindow2.tableWidget.rowCount() + 1
                        )
                        for j, elem in enumerate(row):
                            self.newWindow2.tableWidget.setItem(
                                i, j, QTableWidgetItem(str(elem)))

    def addgenre(self):
        genre, ok_pressed = QInputDialog.getText(self, "Новый жанр",
                                                 "Введите название "
                                                 "жанра")
        if ok_pressed:
            if genre == '':
                self.statusBar().showMessage(
                    'Некорректный ввод')
            else:
                self.connection.cursor().execute(
                    f'INSERT INTO genres(genre) VALUES(?)', (genre,))
                self.connection.commit()
            genres = self.connection.cursor().execute("SELECT * FROM "
                                                      "genres"
                                                      ).fetchall()
            self.TableGenres.setColumnCount(2)
            self.TableGenres.setRowCount(0)
            for i, row in enumerate(genres):
                self.TableGenres.setRowCount(
                    self.TableGenres.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.TableGenres.setItem(
                        i, j, QTableWidgetItem(str(elem)))

    def deleteGenre(self):
        rows = list(
            set([i.row() for i in self.TableGenres.selectedItems()]))
        ids = [self.TableGenres.item(i, 0).text() for i in rows]
        for el in ids:
            res = self.connection.cursor().execute("SELECT * FROM "
                                                   "Read WHERE genre"
                                                   " =?", (el,)
                                                   ).fetchall()
            if not res:
                valid = QMessageBox.question(
                    self, '',
                    "Действительно удалить элементы с id " + ","
                    .join(ids),
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cur = self.connection.cursor()
                    cur.execute(
                        "DELETE FROM genres WHERE id IN (" + ", "
                        .join('?' * len(ids)) + ")", ids)
                    self.connection.commit()

                books = self.connection.cursor().execute("SELECT * "
                                                         "FROM "
                                                         "genres"
                                                         ).fetchall()
                self.TableGenres.setColumnCount(2)
                self.TableGenres.setRowCount(0)
                for i, row in enumerate(books):
                    self.TableGenres.setRowCount(
                        self.TableGenres.rowCount() + 1)
                    for j, elem in enumerate(row):
                        self.TableGenres.setItem(
                            i, j, QTableWidgetItem(str(elem)))
            else:
                self.statusBar().showMessage('Нельзя удалить жанр, '
                                             'который уже '
                                             'используется')

    def addauthor(self):
        author, ok_pressed = QInputDialog.getText(self, "Новый жанр",
                                                  "Введите название "
                                                  "жанра")
        if ok_pressed:
            if author == '':
                self.statusBar().showMessage(
                    'Некорректный ввод')
            else:
                self.connection.cursor().execute(
                    f'INSERT INTO authors(author) VALUES(?)',
                    (author,))
                self.connection.commit()
            authors = self.connection.cursor().execute("SELECT * FROM"
                                                       " authors"
                                                       ).fetchall()
            self.TableAuthors.setColumnCount(2)
            self.TableAuthors.setRowCount(0)
            for i, row in enumerate(authors):
                self.TableAuthors.setRowCount(
                    self.TableAuthors.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.TableAuthors.setItem(
                        i, j, QTableWidgetItem(str(elem)))

    def deleteauthor(self):
        rows = list(
            set([i.row() for i in self.TableAuthors.selectedItems()]))
        ids = [self.TableAuthors.item(i, 0).text() for i in rows]
        for el in ids:
            res = self.connection.cursor().execute("SELECT * FROM "
                                                   "Read WHERE "
                                                   "author =?", (el,)
                                                   ).fetchall()
            if not res:
                valid = QMessageBox.question(
                    self, '',
                    "Действительно удалить элементы с id " +
                    ",".join(ids),
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cur = self.connection.cursor()
                    cur.execute(
                        "DELETE FROM authors WHERE id IN (" + ", "
                        .join('?' * len(ids)) + ")", ids)
                    self.connection.commit()

                authors = self.connection.cursor().execute("SELECT "
                                                           "* FROM "
                                                           "authors"
                                                           ).fetchall(
                )
                self.TableAuthors.setColumnCount(2)
                self.TableAuthors.setRowCount(0)
                for i, row in enumerate(authors):
                    self.TableAuthors.setRowCount(
                        self.TableAuthors.rowCount() + 1)
                    for j, elem in enumerate(row):
                        self.TableAuthors.setItem(
                            i, j, QTableWidgetItem(str(elem)))
            else:
                self.statusBar().showMessage('Нельзя удалить '
                                             'автора, который уже '
                                             'используется')

    def Item_clicked(self, item):
        self.ids = int(self.TableGenres.item(item.row(), 0).text())

    def SaveResultsForGenre(self):
        genre, ok_pressed = QInputDialog.getText(self, "Изменить "
                                                       "жанр",
                                                 "Поменять на:")
        if ok_pressed:
            self.genre = genre
            self.connection.cursor().execute("UPDATE genres"
                                             " SET genre = ?"
                                             "WHERE id = ?",
                                             (self.genre, self.ids))
            self.connection.commit()
        genres = self.connection.cursor().execute("SELECT * FROM "
                                                  "genres").fetchall()
        self.TableGenres.setColumnCount(2)
        self.TableGenres.setRowCount(0)
        for i, row in enumerate(genres):
            self.TableGenres.setRowCount(
                self.TableGenres.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableGenres.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        books = self.connection.cursor().execute("SELECT * FROM "
                                                 "Read").fetchall()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(books):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.FromNumToName()

    def ItemClickedA(self, item):
        self.ids = int(self.TableAuthors.item(item.row(), 0).text())

    def SaveResultsForAuthors(self):
        author, ok_pressed = QInputDialog.getText(self, "Изменить "
                                                        "автора",
                                                  "Поменять на:")
        if ok_pressed:
            self.author = author
            self.connection.cursor().execute("UPDATE authors"
                                             " SET author = ?"
                                             "WHERE id = ?",
                                             (self.author, self.ids))
            self.connection.commit()
        authors = self.connection.cursor().execute("SELECT * FROM "
                                                   "authors"
                                                   ).fetchall()
        self.TableAuthors.setColumnCount(2)
        self.TableAuthors.setRowCount(0)
        for i, row in enumerate(authors):
            self.TableAuthors.setRowCount(
                self.TableAuthors.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableAuthors.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        books = self.connection.cursor().execute("SELECT * FROM "
                                                 "Read").fetchall()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(books):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.FromNumToName()

    def FromNumToName(self):
        cur = self.connection.cursor()
        ids = []
        authors = []
        genre = []
        year = []
        status = []
        for i in range(self.tableWidget.rowCount()):
            ids.append(self.tableWidget.item(i, 2).text())
        for el in ids:
            authors.append(cur.execute("SELECT author FROM authors "
                                       "WHERE id = ? ", (int(el),)
                                       ).fetchall()[0][0])
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 2).setText(str(authors[i]))
        ids.clear()
        for i in range(self.tableWidget.rowCount()):
            ids.append(self.tableWidget.item(i, 4).text())
        for el in ids:
            genre.append(cur.execute("SELECT genre FROM genres "
                                     "WHERE id = ? ", (int(el),)
                                     ).fetchall()[0][0])
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 4).setText(str(genre[i]))
        ids.clear()
        for i in range(self.tableWidget.rowCount()):
            ids.append(self.tableWidget.item(i, 5).text())
        for el in ids:
            year.append(cur.execute("SELECT year FROM years "
                                    "WHERE id = ? ", (int(el),)
                                    ).fetchall()[0][0])
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 5).setText(str(year[i]))
        ids.clear()
        for i in range(self.tableWidget.rowCount()):
            ids.append(self.tableWidget.item(i, 7).text())
        for el in ids:
            status.append(cur.execute("SELECT status FROM statuses "
                                      "WHERE id = ? ", (int(el),)
                                      ).fetchall()[0][0])
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 7).setText(str(status[i]))

    def updateBook(self):
        self.New_Window = MyWidget4()
        self.New_Window.comboBox.addItems(['Название',
                                           'Число страниц', 'Жанр',
                                           'Статус', 'Автор', 'Год',
                                           'Впечатление'])
        if self.NB:
            self.New_Window.Name.setText(self.NB)
            self.New_Window.Author.setText(self.AB)
            self.New_Window.show()
            self.New_Window.pushButton.clicked.connect(self.updateb)

    def updateb(self):
        cur = self.connection.cursor()
        if self.New_Window.comboBox.currentText() == 'Название':
            name = self.New_Window.lineEdit.text()
            if not name:
                self.statusBar().showMessage('Пустое поле')
            else:
                cur.execute("UPDATE Read "
                            "SET name = ? "
                            "WHERE id = ?", (name, self.id))
                self.connection.commit()
        if self.New_Window.comboBox.currentText() == 'Автор':
            author = self.New_Window.lineEdit.text()
            if not author:
                self.statusBar().showMessage('Пустое поле')
            else:
                res = cur.execute("SELECT id FROM authors WHERE "
                                  "author=?", (author,)).fetchall()
                if res:
                    cur.execute("UPDATE Read "
                                "SET author = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
                else:
                    cur.execute(
                        "INSERT INTO authors(author) VALUES(?)",
                        (author,))
                    self.connection.commit()
                    res = cur.execute("SELECT id FROM authors WHERE "
                                      "author=?",
                                      (author,)).fetchall()
                    cur.execute("UPDATE Read "
                                "SET author = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
        if self.New_Window.comboBox.currentText() == 'Число ' \
                                                     'страниц':
            num = self.New_Window.lineEdit.text()
            if not num:
                self.statusBar().showMessage('Пустое поле')
            else:
                cur.execute("UPDATE Read "
                            "SET number_of_pages = ? "
                            "WHERE id = ?", (num, self.id))
                self.connection.commit()
        if self.New_Window.comboBox.currentText() == 'Жанр':
            genre = self.New_Window.lineEdit.text()
            if not genre:
                self.statusBar().showMessage('Пустое поле')
            else:
                res = cur.execute("SELECT id FROM genres WHERE "
                                  "genre=?", (genre,)).fetchall()
                if res:
                    cur.execute("UPDATE Read "
                                "SET genre = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
                else:
                    cur.execute("INSERT INTO genres(genre) VALUES(?)",
                                (genre,))
                    self.connection.commit()
                    res = cur.execute("SELECT id FROM genres WHERE "
                                      "genre=?", (genre,)).fetchall()
                    cur.execute("UPDATE Read "
                                "SET genre = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
        if self.New_Window.comboBox.currentText() == 'Год':
            year = self.New_Window.lineEdit.text()
            if not year:
                self.statusBar().showMessage('Пустое поле')
            else:
                res = cur.execute("SELECT id FROM years WHERE "
                                  "year=?", (int(year),)).fetchall()
                if res:
                    cur.execute("UPDATE Read "
                                "SET year = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
                else:
                    cur.execute("INSERT INTO years(year) VALUES(?)",
                                (int(year),))
                    self.connection.commit()
                    res = cur.execute("SELECT id FROM years WHERE "
                                      "year=?",
                                      (int(year),)).fetchall()
                    cur.execute("UPDATE Read "
                                "SET year = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
        if self.New_Window.comboBox.currentText() == 'Статус':
            status = self.New_Window.lineEdit.text()
            if not status:
                self.statusBar().showMessage('Пустое поле')
            else:
                res = cur.execute("SELECT id FROM statuses WHERE "
                                  "status=?", (status,)).fetchall()
                if res:
                    cur.execute("UPDATE Read "
                                "SET status = ? "
                                "WHERE id = ?",
                                (int(res[0][0]), self.id))
                    self.connection.commit()
                else:
                    self.statusBar().showMessage('Неправильно ввели '
                                                 'статус')
        if self.New_Window.comboBox.currentText() == 'Впечатление':
            opinion = self.New_Window.lineEdit.text()
            cur.execute("UPDATE Read "
                        "SET impression = ? "
                        "WHERE id = ?", (opinion, self.id))
            self.connection.commit()
        books = self.connection.cursor().execute("SELECT * FROM "
                                                 "Read").fetchall()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(books):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        authors = self.connection.cursor().execute("SELECT * FROM aut"
                                                   "hors").fetchall()
        self.TableAuthors.setColumnCount(2)
        self.TableAuthors.setRowCount(0)
        for i, row in enumerate(authors):
            self.TableAuthors.setRowCount(
                self.TableAuthors.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableAuthors.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        genres = self.connection.cursor().execute("SELECT * FROM "
                                                  "genres").fetchall()
        self.TableGenres.setColumnCount(2)
        self.TableGenres.setRowCount(0)
        for i, row in enumerate(genres):
            self.TableGenres.setRowCount(
                self.TableGenres.rowCount() + 1)
            for j, elem in enumerate(row):
                self.TableGenres.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.FromNumToName()
        self.New_Window.hide()

    def elem_clicked(self, item):
        cur = self.connection.cursor()
        self.id = int(self.tableWidget.item(item.row(), 0).text())
        self.NB = cur.execute("SELECT name FROM "
                              "Read WHERE id = ?",
                              (int(self.id),)).fetchall()[0][0]
        self.AB = cur.execute("SELECT author FROM authors WHERE "
                              "id=(SELECT author FROM Read "
                              "WHERE id = ?)",
                              (int(self.id),)).fetchall()[0][0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
