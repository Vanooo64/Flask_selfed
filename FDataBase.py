import sqlite3
import math
import time

class FDataBase:
    def __init__(self, db): #посилання на зв`язок з БД
        self.__db = db #зберыгаэпо посилання у екзампляры данного класу
        self.__cur = db.cursor() #створюэмо клас курсору

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu''' # SQL-запит для отримання всіх записів із таблиці mainmenu
        try:
            self.__cur.execute(sql) # Виконання запиту через курсор
            res = self.__cur.fetchall() # Отримання всіх рядків результату запиту
            if res:
                return res
        except:
            print('Помилка читання БД')
        return []

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?)', (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Помилка додавання статсі в БД' + str(e))
            return False

        return True

    def getPost(self, postID):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {postID} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Помилка додавання статсі в БД' + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Помилка додавання статсі в БД' + str(e))

        return []

