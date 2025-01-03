import _sqlite3
import os #Дозволяє працювати з файловою системою - формувати шляхи до файлів.
import sqlite3
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from  FDataBase import FDataBase

# конфігурація для БД
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'tg573jz4vair8rcp8ug9'

app = Flask(__name__) #створення нового додатку
app.config.from_object(__name__) #загрузка конфігурації БД до додатку
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db'))) #перевизначення шляху до БД

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

@app.teardown_appcontext # коли відбуваеться знннищення контексту додатку
def close_db(error):
    """ЗАкоиває зеднання з БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    menu = dbase.getMenu()
    return render_template('index.html', menu=menu, posts=dbase.getPostsAnonce())

@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    db = get_db() #підеднуеться до БД
    dbase = FDataBase(db) #створюється єкземпляр класу
    menu = dbase.getMenu()

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Помилка додавання статі', category='error')
            else:
                flash('Статя додана успішно', category='success')
        else:
            flash('Помилка додавання статі', category='error')

    return render_template('add_post.html', menu=menu, title='Додавання статі')

@app.route('/post/<alias>')
def showPost(alias):
    db = get_db()  # підеднуеться до БД
    dbase = FDataBase(db)  # створюється єкземпляр класу
    menu = dbase.getMenu()
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=menu, title=title, post=post)

if __name__ == "__main__": #перевіряє, чи скрипт виконується напряму.
    app.run(debug=True) #запускає сервер Flask у режимі розробки (включає автоматичний перезапуск і докладний відладочний вивід у випадку помилок).




# with app.test_request_context(): # створює тимчасовий контекст для тестування додатку без його запуску.
#     print(url_for('about')) #Повертає URL маршруту about (/about) і друкує його в консоль.

