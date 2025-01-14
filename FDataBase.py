import sqlite3
import math
import time
import re

from flask import url_for


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

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print(f"Стаття з таким URL: '{url}' вже існуе")
                return False

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)', (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Помилка додавання статсі в БД' + str(e))
            return False

        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                base = url_for('static', filename='images_html')
                text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                              "\\g<tag>" + base + "/\\g<url>>",
                              res['text'])

                return (res['title'], text)
        except sqlite3.Error as e:
            print('Помилка додавання статсі в БД' + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Помилка додавання статсі в БД' + str(e))

        return []

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Користувач з таким email вже існує")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Помилка додавання користувача в БД  " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email,))
            res = self.__cur.fetchone()
            if not res:
                print("Користувача не знайдено")
                return False

            return res
        except sqlite3.Error as e:
            print("Помилка отримання даннних із БД " + str(e))

        return False


    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Помилка оновлення аватари в БД: " + str(e))
            return False
        return True



