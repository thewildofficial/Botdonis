import discord
from discord.ext import commands
from pyfiglet import Figlet
from replit import db

import traceback
from datetime import datetime
import os

from extensions import coworking
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
    prefix = "%"
    embed_color = ""
    bot_version = ""  # gets updated on_bot_run
    github = "https://github.com/thewildofficial/Botdonis"
    
    # starboard.py utilities
    try:
      reaction_threshhold = db["THRESHHOLD"] # how many reactions to qualify for starring
    except Exception:
      reaction_threshhold = 20
      
    audit_channel_id = int(os.environ["AUDIT_CHANNEL_ID"])
    starboard_channel_id = int(os.environ["STARBOARD_CHANNEL_ID"])
    star_emoji_id = os.environ["STAR_EMOJI_ID"]
    coworking_vc_id = int(os.environ["COWORKING_VC_ID"])
    break_time = int(os.environ["BREAK_TIME"])
    work_time = int(os.environ["WORK_TIME"])
    coworking_channel_id = int(os.environ["COWORKING_CHANNEL_ID"])
    coworking_role_id = int(os.environ["COWORKING_ROLE_ID"])
    guild_id = int(os.environ["GUILD_ID"])    
client = commands.Bot(command_prefix=[BotInformation.prefix],intents=discord.Intents.all(), help_command=EmbedHelpCommand())
for filename in os.listdir("extensions"):
        if filename.endswith(".py"):
            try:
                extname = f"extensions.{filename[:-3]}"
                client.load_extension(extname)
                print(f" * '{extname}'  has been loaded")
            except Exception: traceback.print_exc() 
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
    await client.get_channel(BotInformation.coworking_vc_id).connect() #connects to the VC 
  
    print(f"\n  {client.user} is online and fully functional!")
    


client.run(BotInformation.bot_token)
