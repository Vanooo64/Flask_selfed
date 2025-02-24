import os #Дозволяє працювати з файловою системою - формувати шляхи до файлів.
import sqlite3
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
from  FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from admin.admin import admin

# конфігурація для БД
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'tg573jz4vair8rcp8ug9'
MAX_CONTENT_LENGTH = 1024 * 1024 # мах обєм файлу який можна загрузити на сайт

app = Flask(__name__) #створення нового додатку
app.config.from_object(__name__) #загрузка конфігурації БД до додатку
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db'))) #перевизначення шляху до БД
app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager(app) #створюємо экземпляр классу для користувачів
login_manager.login_view = 'login' #якщо користувач неавторизованний при відвідуванні закритої сторінки він буде перенаправленинй на сторінку авторизаціії
login_manager.login_message = "Для доступу до закритої сторінки необхідно авторизуватися"
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE']) #підключення БД
    conn.row_factory = sqlite3.Row #записи з БД будть представлені у вигляді словника
    return conn

def create_db():
    """Створює БД без запуску веб сервера"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()

def get_db():
    """Зеднання з БД якщо воно ще невстановлене"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    """Встановлення з'єднання з БД перед виконанням запиту"""
    global  dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext # коли відбуваеться знннищення контексту додатку
def close_db(error):
    """ЗАкоиває зеднання з БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    menu = dbase.getMenu()
    return render_template('index.html', menu=menu, posts=dbase.getPostsAnonce())

@app.route('/add_post', methods=['POST', 'GET'])
def addPost():

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Помилка додавання статі', category='error')
            else:
                flash('Статя додана успішно', category='success')
        else:
            flash('Помилка додавання статі', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title='Додавання статі')


@app.route("/post/<alias>")
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated: #перевірка чи користувач авторизований
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit(): # чи були відправленні дані методом POST запиту, превіряэ коректність введених данних
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['password'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for('profile'))

        flash("Неверная пара логин/пароль", "error")

    return render_template('login.html', menu=dbase.getMenu(), title="Авторизація", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            hash = generate_password_hash(form.psw.data)
            res = dbase.addUser(form.name.data, form.email.data, hash)
            if res:
                flash('Ви успішно авторизувалися', 'success')
                return redirect(url_for('login'))
            else:
                flash('Невірно заповненні поля', 'error')

    return render_template('register.html', menu=dbase.getMenu(), title='Регістраця', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з аккаунту', 'success')
    return redirect(url_for('login'))

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', menu=dbase.getMenu(), title='Профіль')

@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename): #verifyExt перевіряє що файл PNG
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Помилка оновлення аватара", "error")
                flash("Аватар оновлено", "success")
            except FileNotFoundError as e:
                flash("Помилка читання файлу", "error")
        else:
            flash("Помилка оновлення аватара", "error")

    return redirect(url_for('profile'))


if __name__ == "__main__": #перевіряє, чи скрипт виконується напряму.
    app.run(debug=True) #запускає сервер Flask у режимі розробки (включає автоматичний перезапуск і докладний відладочний вивід у випадку помилок).


# with app.test_request_context(): # створює тимчасовий контекст для тестування додатку без його запуску.
#     print(url_for('about')) #Повертає URL маршруту about (/about) і друкує його в консоль.

