# Coworking VC utilities 
import discord
from replit import db
from discord.ext import commands
from bot import BotInformation
import asyncio

class Coworking(commands.Cog):
  #initialize client class
    def __init__(self, client):
        self.client = client
        self.is_working = False
        client.loop.create_task(self.pomo_clock())

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):  
      if member.voice == None:
        try:
          await member.remove_roles(self.client.get_guild(BotInformation.guild_id).get_role(BotInformation.coworking_role_id))
          await member.edit(mute=False)
        except Exception as e:
          pass
      
      elif member.voice.channel != self.client.get_channel(BotInformation.coworking_vc_id):
        try:
          await member.remove_roles(self.client.get_guild(BotInformation.guild_id).get_role(BotInformation.coworking_role_id))
          await member.edit(mute=False)
        except Exception as e:
          pass

      elif member.voice.channel == self.client.get_channel(BotInformation.coworking_vc_id) and member != self.client.user:
          try:
            await member.add_roles(self.client.get_guild(BotInformation.guild_id).get_role(BotInformation.coworking_role_id))
            await member.edit(mute=self.is_working)
          except Exception:
            pass
  
        
      
      
          
    
    
    async def mute_switcher(self,mode):
      try:
        for member in self.client.get_channel(BotInformation.coworking_vc_id).members:
          if member != self.client.user:
            await member.edit(mute=mode)
      except Exception as e:
        # print(e)
        pass

    
    
    
    async def set_break(self):
      self.is_working = False
      # unmutes everyone in voice channel
      await self.mute_switcher(self.is_working)
      # play audio indicating break time
      try:
        await self.client.get_channel(BotInformation.coworking_channel_id).send(f"Session ended! Break time of duration {BotInformation.break_time} starts now.")
        # remove slow mode
        await self.client.get_channel(BotInformation.coworking_channel_id).edit(slowmode_delay=0)
      except Exception as e:
        pass
        
    async def set_working(self):
      self.is_working = True
      # mutes everyone in voice channel
      await self.mute_switcher(self.is_working)
      # play audio that indicates working time

      try:
        # send a message in coworking chat that lasts for about 10 mins,which says that the work time has started
        confirmation_message = await self.client.get_channel(BotInformation.coworking_channel_id).send(f"Work time of duration {BotInformation.work_time} minutes started. React to this message with :raised_hand: to verify that you are not AFK (note: if you dont react you can get kicked for inactivity!)",delete_after= 10 * 60)
        # adds reactions to confirmation_message
        await confirmation_message.add_reaction("✋")
        # Turn on slow mode in the coworking chat (10 seconds)
        await self.client.get_channel(BotInformation.coworking_channel_id).edit(slowmode_delay=10) 
      except Exception:
        pass 
      

      
    async def pomo_clock(self):
      # Sets up an async loop in which set_working() and set_break() runs repeatedly
      while True:
        await self.set_working()
        #await asyncio.sleep(BotInformation.work_time * 60)
        await asyncio.sleep(5)
        await self.set_break()
        await asyncio.sleep(5)
        #await asyncio.sleep(BotInformation.break_time)
       
        


def setup(client):
    client.add_cog(Coworking(client))

