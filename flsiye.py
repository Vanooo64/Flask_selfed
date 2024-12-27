from flask import Flask, render_template, url_for

app = Flask(__name__)
menu = ['Встановлення', 'Перший додаток', 'Зворотній звязок']


@app.route("/")
@app.route("/index")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title='Про сайт', menu=menu)

@app.route("/profile/<username>")
def profile(username, path):
    return f"Користувач: {username}, {path}"


with app.test_request_context():
    print(url_for('index'))
    print(url_for('about'))
    print(url_for('profile', username='ivan'))


# with app.test_request_context(): # створює тимчасовий контекст для тестування додатку без його запуску.
#     print(url_for('about')) #Повертає URL маршруту about (/about) і друкує його в консоль.

# if __name__ == "__main__": #перевіряє, чи скрипт виконується напряму.
#     app.run(debug=True) #запускає сервер Flask у режимі розробки (включає автоматичний перезапуск і докладний відладочний вивід у випадку помилок).