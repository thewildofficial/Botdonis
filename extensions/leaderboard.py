import discord
from replit import db
from discord.ext import commands
from bot import BotInformation
class Leaderboard(commands.Cog):
  #initialize client class
    def __init__(self, client):
        self.client = client 
    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
      raw_lb = {}
      for key in db:
        try:
          int(key) # if key is not int, this should through an exception
          raw_lb[key] = db[key]["score"]
        except Exception as e: pass
      sorted_lb = {k: v for k, v in sorted(raw_lb.items(), key=lambda x: x[1],reverse=True)}
      
      lb_embed = discord.Embed(title="Current Leaderboard", description="rankings based on how valuable messages made by users are. \n level up by posting more meaningful content around the server and accumulating as many STARPOINTS around the server!", color= BotInformation.embed_color)
      lb_embed.set_thumbnail(url=ctx.guild.icon_url)
      rank = 1 #initial rank 
      for user_id in sorted_lb: 
        if rank <= 5:
              lb_embed.add_field(name= f" {rank}. {self.client.get_user(int(user_id))}",value= "test", inline=False)
              rank+=1
      await ctx.send(embed=lb_embed)
      

def setup(client):
    client.add_cog(Leaderboard(client))