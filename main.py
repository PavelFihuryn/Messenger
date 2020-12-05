import json
import time
from datetime import datetime


def set_message():
    message = {'name': 'Jan', 'text': 'None', 'time': time.time()}
    message['text'] = input(message['name'])
    write_json(message)


def get_message(messages, moment):
    for message in messages:
        if message['time'] < moment:
            print_message(message)


def write_json(new_message):
    try:
        messages = json.load(open('message.json'))
    except:
        messages = []
    messages.append(new_message)
    with open("message.json", "w") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


def print_message(message):
    beauty_time = datetime.fromtimestamp(message['time'])
    beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M')
    print(beauty_time, message['name'])
    print(message['text'])


if __name__ == "__main__":
    set_message()
    set_message()
    set_message()
    file = json.load(open('message.json'))
    get_message(file, time.time())
