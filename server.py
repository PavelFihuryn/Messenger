import subprocess
import time
import webbrowser

from flask import Flask, request
from datetime import datetime
import json

from werkzeug.exceptions import abort

app = Flask(__name__)


def write_json(new_message):
    try:
        messages = json.load(open('message.json'))
    except:
        messages = []
    messages.append(new_message)
    with open("message.json", "w") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


@app.route('/')
def index():
    return '<h1>Hello</h1>'


def statistics():
    number_messages = []
    file = json.load(open('message.json'))
    for message in file:
        if message['name'] not in number_messages:
            number_messages.append(message['name'])
    return len(number_messages), len(file)


@app.route('/status')
def status():
    number_users, number_messages = statistics()
    stat = {
        'status': True,
        'name': 'MessaGa',
        'time': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'number_users': number_users,
        'number_messages': number_messages
    }
    return json.dumps(stat, indent=4)


@app.route('/messages')
def get_messages():
    try:
        after = float(request.args.get('after', 0))
    except ValueError:
        return abort(400)
    messages = []
    for message in json.load(open('message.json')):
        if message['time'] > after:
            messages.append(message)
    return {'messages': messages}


@app.route('/send', methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json['name']
    text = request.json['text']

    if not (isinstance(name, str)
            and isinstance(text, str)
            and name
            and text):
        return abort(400)

    # Бот запросы
    if text[0] == '/':
        words = text.split()
        key = words[0]
        value = ''
        for i in range(1, len(words)):
            value += ' ' + words[i]
        if key == '/date':  # Показать текущую дату
            text = datetime.now().strftime('%d %B, %Y')
            name = 'bot'
        if key == '/google':  # Открыть браузер и спросить у Гугла
            webbrowser.open_new_tab('https://www.google.com/search?q=' + value)
            return {'Ok': True}
        if key == '/wiki':  # Открыть браузер и спросить у Википедии
            webbrowser.open_new_tab('https://ru.wikipedia.org/wiki/' + value)
            return {'Ok': True}
        if key == '/calendar':  # Показать значимые даты на сегодня
            text = subprocess.check_output('calendar').decode("utf-8")
            name = 'bot'
        if key == '/help':  # Список команд бота
            with open('help.txt', 'r') as help_command:
                text = help_command.read()
            name = 'bot'
        if key == '/stat':  # Статистика чата
            number_users, number_messages = statistics()
            text = f'Пользователей: {number_users}, сообщений {number_messages}'
            name = 'bot'

    new_message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    write_json(new_message)
    return {'Ok': True}


if __name__ == '__main__':
    app.run(debug=True)
