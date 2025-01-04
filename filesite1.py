import datetime
import datetime
from flask import Flask, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '924f0adbb01c7b8fe6772835871f2a680f85b42c'
app.permanent_session_lifetime = datetime.timedelta(days=10)

@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # обновление данных сессии
    else:
        session['visits'] = 1  # запись данных в сессию

    return f"<h1>Main Page</h1>Число переглядів: {session['visits']}"


data = [1, 2, 3, 4]
@app.route("/session")
def session_data():
    session.permanent = True
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True

    return f"session['data']: {session['data']}"


if __name__ == "__main__": #перевіряє, чи скрипт виконується напряму.
    app.run(debug=True) #запускає сервер Flask у режимі розробки (включає автоматичний перезапуск і докладний відладочний вивід у випадку помилок).
