import discord
from discord.ext import commands
from bot import BotInformation

class General(commands.Cog):
    """General utility commands"""
    #initialize client class
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        """ 🔍 displays general information about the bot"""
  

    @commands.Cog.listener()
    async def on_message(self, message):
        #returns the prefix
        mention = f'<@!{self.client.user.id}>'
        if mention in message.content and message.author.id != self.client.user.id:
            await message.channel.send(f'Current command for {mention} is `{BotInformation.prefix}`')

  
def setup(client):
    client.add_cog(General(client))


