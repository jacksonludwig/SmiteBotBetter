import utils
import scrape_data
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
        data = []
        if len(args) == 1:
            data = scrape_data.get_results(god_name, args[0])
        else:
            data = scrape_data.get_results(god_name, "conquest")

        if data[0] == CONST_PRO_MARKER:
            embed1 = utils.make_pro_embed_start(
                god_name.upper(), data, CONST_START_SEPEARATOR)
            embed2 = utils.make_pro_embed_end(god_name.upper(), data)
            await context.send(embed=embed1)
            await context.send(embed=embed2)
        else:
            embed = utils.make_generic_embed(god_name.upper(), data)
            await context.send(embed=embed)
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
