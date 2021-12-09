import discord
from replit import db
from discord.ext import commands
from bot import BotInformation
class Starboard(commands.Cog):
  #initialize client class
    def __init__(self, client):
        self.client = client
    
    async def threshhold_builder(self):
      return 1
    async def get_points(self,message):
      points = 0
      for reaction in message.reactions:
        if BotInformation.star_emoji_id == reaction.emoji.id:
          async for user in reaction.users():
            if str(user.roles[len(user.roles)-1].id) in BotInformation.rank_points.keys():
              points += rank_points[str(user.roles[len(user.roles)-1]).id]  
      return points

	# interacts with the database to update score
    def increase_points(self, discord_id,points): 
      discord_id = str(discord_id)
      points = int(points)
      if discord_id in db.keys():
            db[f"star_{discord_id}"]["score"] = db[f"star_{discord_id}"]["score"] + points # increases the current db score by points
      else:
            db[f"star_{discord_id}"] = {"score":points}  # initializes a new score
    
    # gets the number of points in a message 
    @commands.command(aliases=["pc"])
    async def pointscount(self,ctx):
      '''Returns the number of points that are attributed to a message (you must reply to one!). alias: pc'''
      message = ctx.message.reference.resolved
      points = 0
      for reaction in message.reactions:
        if reaction.emoji.id == BotInformation.star_emoji_id:
          for user in reaction.users:
            print(user.roles)
            points += BotInformation.rank_points[user.roles[str(len(user.roles)-1)].id] 
      await message.reply(f"This message is worth {points} points.") 

      

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        # Tracks every single reaction in the server        
       
        users = await reaction.users().flatten() 
        #if reaction.message.author in users:
            # if the reaction author is a reacter,remove their reaction
        #    await reaction.message.remove_reaction(self.client.get_emoji(int(BotInformation.star_emoji_id)),reaction.message.author)
       
        if reaction.count == await self.threshhold_builder() and reaction.emoji == self.client.get_emoji(int(BotInformation.star_emoji_id)):
            '''
        checks if the number of reactions is  equal to the required amount
        checks if the reaction sent qualifies for the starboard
        '''
            '''if str(reaction.message.author.roles[len(user.roles)-1].id) in BotInformation.rank_points.keys():
              points = BotInformation.rank_points[str(reaction.message.author.roles[len(user.roles)-1].id)]
            else: points = 0
            self.increase_points(reaction.message.author.id,points)'''

            starboard_embed=discord.Embed(color=reaction.message.author.roles[len(user.roles)-1].color,description=f"{reaction.message.content}")
            starboard_embed.set_author(name = reaction.message.author.name, icon_url= reaction.message.author.avatar_url)
            starboard_message = await self.client.get_channel(BotInformation.starboard_channel_id).send(embed=starboard_embed)
        
       

def setup(client):
    client.add_cog(Starboard(client))


