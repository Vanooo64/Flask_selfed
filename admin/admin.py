from flask import Blueprint, render_template, request, url_for, redirect, flash, session

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
        {'url': '.logout', 'title': 'Выйти'}]

@admin.route('/')
def index():
    if isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Адмін-панель')

@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
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
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))
