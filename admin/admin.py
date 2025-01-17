import sqlite3

from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
"""'admin' – ім'я Blueprint, яке буде суфіксом до всіх імен методів даного модуля;
__name__ – ім'я модуля, щодо якого буде шукатися папка admin і відповідні підкаталоги; 
template_folder – підкаталог шаблонів даного Blueprint (необов'язковий параметр, за його відсутності береться підкаталог шаблонів докладання); 
static_folder – підкаталог статичних файлів (необов'язковий параметр, за його відсутності береться підкаталог static докладання)."""

def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.listpubs', 'title': 'Статі'},
        {'url': '.listusers', 'title': 'Користувачі'},
        {'url': '.logout', 'title': 'Выйти'}]

db = None
@admin.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request

@admin.route('/')
def index():
    if not isLogged():  # Якщо користувач не авторизований
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Адмін-панель')

@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():  # Якщо користувач вже авторизований
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Невірна пара логін/пароль", "error")

    return render_template('admin/login.html', title='Адмін-панель')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():  # Якщо користувач не авторизований
        return redirect(url_for('.login'))

    logout_admin()  # Вихід із системи
    return redirect(url_for('.login'))


@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Помилка отримання статей із БД " + str(e))

    return render_template('admin/listpubs.html', title='Список статей', menu=menu, list=list)

@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Помилка отримання користувачів із БД " + str(e))

    return render_template('admin/listusers.html', title='Список користувачів', menu=menu, list=list)
