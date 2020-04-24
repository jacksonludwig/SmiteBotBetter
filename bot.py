import utils
import discord
from discord.ext import commands

CONST_PRO_MARKER = "PRO"
CONST_START_SEPEARATOR = "SEPARATOR"

client = commands.Bot(command_prefix="#")
client.remove_command("help")


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


@client.command()
async def help(context):
    await context.send(embed=utils.make_info_embed())


@client.event
async def on_message(message):
    utils.log_messages(message)

    if message.author == client.user:
        return

    await client.process_commands(message)


def main():
    client.run(utils.get_token())


main()
