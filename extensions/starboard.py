import discord
from replit import db
from discord.ext import commands
from bot import BotInformation
class Starboard(commands.Cog):
  #initialize client class
    def __init__(self, client):
        self.client = client
	# interacts with the database to update score
    def increase_points(self, discord_id,points): 
      discord_id = str(discord_id)
      if discord_id in db.keys():
            db[discord_id]["score"] = db[discord_id]["score"] + points # increases the current db score by one
      else:
            db[discord_id] = {"score":points}  # initializes a new score
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        # Tracks every single reaction in the server        
       
        users = await reaction.users().flatten() 
        #if reaction.message.author in users:
            # if the reaction author is a reacter,remove their reaction
         #   await reaction.message.remove_reaction(self.client.get_emoji(int(BotInformation.star_emoji_id)),reaction.message.author)
       
        if reaction.count == BotInformation.reaction_threshhold and reaction.emoji == self.client.get_emoji(int(BotInformation.star_emoji_id)):
            '''
        checks if the number of reactions is  equal to the required amount
        checks if the reaction sent qualifies for the starboard
        '''
            self.increase_points(reaction.message.author.id,1)
            audit_embed=discord.Embed(title="Click to jump to message!", url= reaction.message.jump_url, color=user.roles[len(user.roles)-1].color)
            audit_embed.set_author(name = reaction.message.author.name , icon_url= reaction.message.author.avatar_url)
            audit_embed.add_field(name="message content:", value=f"{reaction.message.content}", inline=True)
            audit_message = await self.client.get_channel(BotInformation.audit_channel_id).send(embed=audit_embed)
            for emoji in ["✅","❌"]:
                await audit_message.add_reaction(emoji)
        
        # Logic for the audit channel
        elif reaction.message.channel.id == BotInformation.audit_channel_id and not self.client.user == user:
            # checks if the reaction is coming from the auditing channel
            if reaction.emoji == "✅":
                # sends embed to the starred channel,and deletes the auditing message
               await self.client.get_channel(BotInformation.starboard_channel_id).send(embed=reaction.message.embeds[0])
               await reaction.message.delete()
               self.increase_points(reaction.message.author.id,2)
            elif reaction.emoji == "❌":
                # just deletes the audit Message
                await reaction.message.delete()

def setup(client):
    client.add_cog(Starboard(client))


