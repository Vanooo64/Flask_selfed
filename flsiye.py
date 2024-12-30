from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tg573jz4vair8rcp8ug9'

menu = [{"name": "Встановлення", "url": "install-flask"},
        {"name": "Перший додаток", "url": "first-app"},
        {"name": "Зворотній звязок", "url": "contact"},
        {"name": "Увійти", "url": "login"}]


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', menu=menu)

@app.route("/about")
def about():
    return render_template('about.html', title='Про сайт', menu=menu)

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        username = request.form.get('username')
        if username and len(username) > 2:  # якщо користувач у полі Імя ннабрав > 2 символів
            flash('Повідомлення відправлено', category='seccess')  # ідображаеться повідомлення
        else:
            flash('Помилка відправки', category='error')

    return render_template('contact.html', title='Зворотній звязок', menu=menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профіль корисстувача: {username}!"
    # return render_template('profile.html', title='Про сайт', menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизація', menu=menu)

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title='Сторінка незннайдена', menu=menu), 404



# @app.route("/profile/<username>")
# def profile(username, path):
#     return f"Користувач: {username}, {path}"
#
#
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='ivan'))


# with app.test_request_context(): # створює тимчасовий контекст для тестування додатку без його запуску.
#     print(url_for('about')) #Повертає URL маршруту about (/about) і друкує його в консоль.

if __name__ == "__main__": #перевіряє, чи скрипт виконується напряму.
    app.run(debug=True) #запускає сервер Flask у режимі розробки (включає автоматичний перезапуск і докладний відладочний вивід у випадку помилок).