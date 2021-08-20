import discord
from discord.ext import commands
from bot import BotInformation
from replit import db
class General(commands.Cog):
    """General utility commands"""
    #initialize client class
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_threshhold(self,ctx,number):
      """ADMIN ONLY: set the number of reactions required for the starboard."""
      try:
        db["THRESHHOLD"] = int(number)
        await ctx.send(f"Number of reactions required set to `{number}`!")
      except Exception:
        await ctx.send("You must input a number!")
    @commands.command()
    async def info(self, ctx):
        """ 🔍 displays general information about the bot"""
        embed = discord.Embed(
            description="Botdonis is a custom bot made for Hamza Ahmed's discord server.",
            color=BotInformation.embed_color)
        embed.set_author(name=self.client.user, url=BotInformation.github,
                         icon_url=self.client.user.avatar_url)
        embed.add_field(name="Version", value=BotInformation.bot_version, inline=True)
        embed.add_field(name="Github", value=BotInformation.github, inline=True)
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        #returns the prefix
        mention = f'<@!{self.client.user.id}>'
        if mention in message.content and message.author.id != self.client.user.id:
            await message.channel.send(f'Current command for {mention} is `{BotInformation.prefix}`')

def setup(client):
    client.add_cog(General(client))


