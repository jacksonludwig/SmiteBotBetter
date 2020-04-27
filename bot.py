import utils
import discord
from discord.ext import commands
import god_item_puller
import db_connector

client = commands.Bot(command_prefix="#")
client.remove_command("help")

god_dict = god_item_puller.get_dictionary_for_bot()


@client.event
async def on_ready():
    print("Smite bot is now running...")


@client.command()
async def build(context, god_name):
    await context.send("querying...")
    name = utils.replace_dashes_with_spaces(god_name)
    try:
        build = db_connector.query_build_by_name(god_dict, name)

        embed = discord.Embed(
            title=f"BUILD: {god_name.upper()}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Core Build",
                        value=utils.organize_build_for_embed(build[0]), inline=False)
        embed.add_field(name="Offensive Options",
                        value=utils.organize_build_for_embed(build[1]), inline=False)
        embed.add_field(name="Defensive Options",
                        value=utils.organize_build_for_embed(build[2]), inline=False)
        embed.set_footer(text="data from smite.gg")

        await context.send(embed=embed)
    except Exception as e:
        print(e)
        await context.send("scraping failed (check god name)")


@client.command()
async def help(context):
    embed = discord.Embed(
        title=f"HELP",
        color=discord.Color.green()
    )
    embed.add_field(
        name="#build", value="Say #build followed by god name, e.g.\n \"#build anubis\"")

    embed.set_footer(text="https://github.com/ludwj61/SmiteBotBetter")

    await context.send(embed=embed)


@client.event
async def on_message(message):
    # utils.log_messages(message)

    if message.author == client.user:
        return

    await client.process_commands(message)


def main():
    client.run(utils.get_token())


main()
