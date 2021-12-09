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
        self.confirmed_users = []
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


    def add_time(self):
      #adds points to leaderboard for people in self.confirmed_users
      
      for user in self.confirmed_users:
        try:
          db[f"vc_{user.id}"] = db[f"vc_{user.id}"] + BotInformation.work_time
        except Exception:
          db[f"vc_{user.id}"] = BotInformation.work_time
          
          

    async def set_break(self):
      self.add_time()
      self.is_working = False
      # unmutes everyone in voice channel
      await self.mute_switcher(self.is_working)
      # play audio indicating break time
      self.client.get_guild(int(BotInformation.guild_id)).voice_client.play(discord.FFmpegPCMAudio("audio/break.mp3"))
      try:
        await self.client.get_channel(BotInformation.coworking_channel_id).send(f"<@&{BotInformation.coworking_role_id}> Session ended! Break time of duration {BotInformation.break_time} minutes starts now.",delete_after= 2*60)
        # remove slow mode
        await self.client.get_channel(BotInformation.coworking_channel_id).edit(slowmode_delay=0)
      except Exception as e:
        pass



    async def set_working(self):
      self.confirmed_users = []
      self.is_working = True
      # mutes everyone in voice channel
      await self.mute_switcher(self.is_working)
      # play audio that indicates working time
      self.client.get_guild(int(BotInformation.guild_id)).voice_client.play(discord.FFmpegPCMAudio("audio/work.mp3"))
      try:
        # Turn on slow mode in the coworking chat (10 seconds)
        await self.client.get_channel(BotInformation.coworking_channel_id).edit(slowmode_delay=10) 
        
        # send a message in coworking chat that lasts for about 10 mins,which says that the work time has started
        confirmation_message = await self.client.get_channel(BotInformation.coworking_channel_id).send(f"<@&{BotInformation.coworking_role_id}> Work time of duration {BotInformation.work_time} minutes started. ")
      except Exception:
        pass 
      

      
    async def pomo_clock(self):
      # Sets up an async loop in which set_working() and set_break() runs repeatedly
      await asyncio.sleep(10)
      while True:
        await self.set_working()
        #await asyncio.sleep(BotInformation.work_time * 60)
        await asyncio.sleep(20)
        await self.set_break()
        #await asyncio.sleep(BotInformation.break_time * 60)
        await asyncio.sleep(20)
        
        

       
        


def setup(client):
    client.add_cog(Coworking(client))

