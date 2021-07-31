import typing
import discord
from discord.ext import commands
from bot import BotInformation
class Starboard(commands.Cog):
  #initialize client class
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        # Tracks every single reaction in the server
        if reaction.count == BotInformation.reaction_threshhold and reaction.emoji.id == BotInformation.star_emoji_id and not user == reaction.message.author:
            '''
        checks if the number of reactions is  equal to the required amount
        checks if the reaction sent qualifies for the starboard
        checks if the reacter is not the same person as the message auther
        '''
            audit_embed=discord.Embed(title="Click to jump to message!", url= reaction.message.jump_url, description=f"Created at {reaction.message.created_at} UTC", color=BotInformation.embed_color)
            audit_embed.set_author(name = reaction.message.author.name , icon_url= reaction.message.author.avatar_url)
            audit_embed.add_field(name="message content:", value=f"```{reaction.message.content}```", inline=True)
            audit_message = await self.client.get_channel(BotInformation.audit_channel_id).send(embed=audit_embed)
            for emoji in ["✅","❌"]:
                await audit_message.add_reaction(emoji)
        # Logic for the audit channel
        if reaction.message.channel.id == BotInformation.audit_channel_id:
            # checks if the reaction is coming from the auditing channel
            if reaction.emoji == "✅":
                # sends embed to the starred channel,and deletes the auditing message
               await self.client.get_channel(BotInformation.starboard_channel_id).send(embed=reaction.message.embeds[0])
               await reaction.message.delete()
            elif reaction.emoji == "❌":
                # just deletes the audit Message
                await reaction.message.delete()

def setup(client):
    client.add_cog(Starboard(client))


