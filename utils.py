import json


def get_token():
    with open("token.json") as file:
        data = json.load(file)
        return data["token"]


def log_messages(message):
    print(F'Message from {message.author}: {message.content}')


def read_names(file_name):
    with open(file_name, encoding="utf-8") as file:
        names = [line.rstrip() for line in file.readlines()]
    return names
