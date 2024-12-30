import _sqlite3
import os #Дозволяє працювати з файловою системою - формувати шляхи до файлів.
import sqlite3

from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g

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
    if not hasattr(g, 'link.db'):
        g.link_db = connect_db()
    return g.link_db

@app.route("/")
def index():
    db = get_db()
    return render_template('index.html', menu = [])

@app.teardown_appcontext # коли відбуваеться знннищення контексту додатку
def close_db(error):
    """ЗАкоиває зеднання з БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()



# menu = [{"name": "Встановлення", "url": "install-flask"},
#         {"name": "Перший додаток", "url": "first-app"},
#         {"name": "Зворотній звязок", "url": "contact"},
#         {"name": "Увійти", "url": "login"}]


# @app.route("/")
# @app.route("/index")
# def index():
#     return render_template('index.html', menu=menu)
#
# @app.route("/about")
# def about():
#     return render_template('about.html', title='Про сайт', menu=menu)
#
# @app.route("/contact", methods=['POST', 'GET'])
# def contact():
#     if request.method == "POST":
#         username = request.form.get('username')
#         if username and len(username) > 2:  # якщо користувач у полі Імя ннабрав > 2 символів
#             flash('Повідомлення відправлено', category='seccess')  # ідображаеться повідомлення
#         else:
#             flash('Помилка відправки', category='error')
#
#     return render_template('contact.html', title='Зворотній звязок', menu=menu)
#
# @app.route("/profile/<username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"Профіль корисстувача: {username}!"
#     # return render_template('profile.html', title='Про сайт', menu=menu)
#
#
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == "POST" and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     return render_template('login.html', title='Авторизація', menu=menu)
#
# @app.errorhandler(404)
# def pageNotFount(error):
#     return render_template('page404.html', title='Сторінка незннайдена', menu=menu), 404


#
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='ivan'))


# with app.test_request_context(): # створює тимчасовий контекст для тестування додатку без його запуску.
#     print(url_for('about')) #Повертає URL маршруту about (/about) і друкує його в консоль.

if __name__ == "__main__": #перевіряє, чи скрипт виконується напряму.
    app.run(debug=True) #запускає сервер Flask у режимі розробки (включає автоматичний перезапуск і докладний відладочний вивід у випадку помилок).