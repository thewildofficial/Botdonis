import discord
from discord.ext import commands
from pyfiglet import Figlet

from datetime import datetime
import os

class EmbedHelpCommand(commands.MinimalHelpCommand):
    """builds embed for help command"""

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page,color=BotInformation.embed_color)
            await destination.send(embed=embed)


class BotInformation:
    # all the information used by the Cogs to be stored here
    bot_token = os.environ["BOT_TOKEN"]
    prefix = "$"
    embed_color = ""
    bot_version = ""  # gets updated on_bot_run
    github = "https://github.com/thewildofficial/Botdonis"
    
    # starboard.py utilities
    reaction_threshhold = 50 # how many reactions to qualify for starring
    audit_channel_id = os.environ["AUDIT_CHANNEL_ID"]
    starboard_channel_id = os.environ["STARBOARD_CHANNEL_ID"]
    star_emoji_id = os.environ["STAR_EMOJI_ID"]

intents = discord.Intents.default()
client = commands.Bot(command_prefix=[BotInformation.prefix], intent=intents, help_command=EmbedHelpCommand())
intents.members = True
for filename in os.listdir("extensions"):
        if filename.endswith(".py"):
            try:
                extname = f"extensions.{filename[:-3]}"
                client.load_extension(extname)
                print(f" * '{extname}'  has been loaded")
            except Exception as e: print(e)

# starting
@client.event
async def on_ready():
    print(Figlet().renderText('BOTDONIS'))
    BotInformation.bot_version = f"v{len(client.commands) / 10}"
    BotInformation.embed_color = client.user.color
    print(
        f'\n * Logged in as {client.user.name}#{client.user.discriminator} \n * Time: {datetime.now()}')
    await client.change_presence(
        activity=discord.Game(name="Delayed Gratification Grindset"),
        status=discord.Status.dnd
    )
    print(f"\n  {client.user} is online and fully functional!")


client.run(BotInformation.bot_token)
