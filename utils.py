import json
import discord
from discord.ext import commands

sep_index = 0

def get_token():
    with open("token.json") as file:
        data = json.load(file)
        return data["token"]


def log_messages(message):
    print('Message from {0.author}: {0.content}'.format(message))


def make_footer(embed, foot_text):
    embed.set_footer(text=foot_text)


def make_pro_embed_start(god_name, data, CONST_START_SEPEARATOR):
    embed = discord.Embed(
        title="{}: Starting build".format(god_name),
        color=discord.Color.blue()
    )
    global sep_index
    for i in range(1, len(data)):
        if data[i] == CONST_START_SEPEARATOR:
            sep_index = i
            break
        embed.add_field(name="{}.)".format(
            i), value=data[i])

    make_footer(embed, "source: smite.guru")
    return embed


def make_pro_embed_end(god_name, data):
    embed = discord.Embed(
        title="{}: Ending build".format(god_name),
        color=discord.Color.red()
    )
    global sep_index
    for i in range(sep_index + 1, len(data)):
        embed.add_field(name="{}.)".format(
            i - sep_index), value=data[i])

    make_footer(embed, "source: smite.guru")
    return embed


def make_generic_embed(god_name, data):
    embed = discord.Embed(
        title="{}: Build".format(god_name),
        color=discord.Color.green()
    )
    for i in range(len(data)):
        embed.add_field(name="{}.)".format(
            i + 1), value=data[i])

    make_footer(embed, "source: smite.guru")
    return embed


def make_info_embed():
    embed = discord.Embed(
        title="Smite Build Bot",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Use", value="Type a hash and build (#build) followed by a god name and \
        then a game mode, e.g. \n\"#build loki conquest\"")
    return embed
