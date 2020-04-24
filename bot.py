import utils
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="#")


@client.event
async def on_ready():
    print("Smite bot is now running...")


@client.command()
async def build(context, god_name, *args):
    try:
        await context.send("scraping...")
        # post the build here
    except:
        await context.send("scraping failed (check god and/or game mode)")


@client.event
async def on_message(message):
    utils.log_messages(message)

    if message.author == client.user:
        return

    await client.process_commands(message)


def main():
    client.run(utils.get_token())


main()
