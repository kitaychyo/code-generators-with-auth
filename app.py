from secrets import randbelow

from flask import Flask, jsonify, request

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="ru">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Генератор кода — вход</title>
<body style="font-family: sans-serif; text-align: center; margin: 80px 20px">
  <h1>Генератор кода</h1>
  <form id="login">
    <p>Логин: <b>demo</b> · Пароль: <b>demo</b></p>
    <p><label>Логин <input name="username" autocomplete="username" required></label></p>
    <p><label>Пароль <input name="password" type="password" autocomplete="current-password" required></label></p>
    <button>Войти</button>
  </form>
  <p id="message" role="status"></p>
  <section id="result" hidden>
    <p id="code" style="font-size: 48px"></p>
    <p>Обновление страницы завершит вход.</p>
    <a href="/">Выйти</a>
  </section>
  <script>
    const form = document.getElementById('login');
    const message = document.getElementById('message');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const button = form.querySelector('button');
      button.disabled = true;
      message.textContent = '';
      try {
        const response = await fetch('/login', {method: 'POST', body: new FormData(form)});
        const data = await response.json();
        if (!response.ok) {
          message.textContent = data.error;
          return;
        }
        form.reset();
        form.hidden = true;
        document.getElementById('code').textContent = data.code;
        document.getElementById('result').hidden = false;
      } catch {
        message.textContent = 'Ошибка соединения. Попробуй ещё раз.';
      } finally {
        button.disabled = false;
      }
    });
    window.addEventListener('pageshow', (event) => {
      if (event.persisted) location.reload();
    });
  </script>
</body>
</html>
"""


@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.get('/')
def index():
    return HTML


@app.post('/login')
def login():
    if request.form.get('username') != 'demo' or request.form.get('password') != 'demo':
        return jsonify(error='Неверный логин или пароль.'), 401
    return jsonify(code=randbelow(9000) + 1000)


if __name__ == '__main__':
    app.run()
