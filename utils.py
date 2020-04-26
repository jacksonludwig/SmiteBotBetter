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


def make_singleton_tuples(names):
    for i in range(len(names)):
        names[i] = (names[i],)


def replace_spaces_with_dashes(names):
    for i in range(len(names)):
        names[i] = names[i].replace(" ", "-")


def replace_space_with_dash(name):
    return name.replace(" ", "-")


def replace_dashes_with_spaces(name):
    return name.replace("-", " ")


def remove_non_letters(name):
    return ''.join([char for char in name if char.isalpha() or char == " " or char == "-"])


def create_dictionary_from_list(names):
    name_dict = {}
    count = 1
    for name in names:
        name_dict.update({name: count})
        count = count + 1
    return name_dict


def find_id_by_name(name_dict, name):
    name = name.strip().lower()
    for god_name, ident in name_dict.items():
        if god_name.strip().lower() == name:
            return ident


def organize_build_for_embed(items):
    build_string = ""
    for item in items:
        build_string = build_string + item + "\n"
    return build_string
