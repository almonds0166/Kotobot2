
import asyncio
import random
from datetime import datetime, timedelta

from discord.ext import commands, tasks
import pytz

import sys; sys.path.append("..")
from util import get_moon_info, get_moon_emoji, get_moon_summary, remember

class Lunar(commands.Cog):
   """Behavior that has to do with phases of the moon"""
   def __init__(self, bot):
      self.bot = bot
      self.check_moon_phase.start()

   @commands.Cog.listener()
   async def on_message(self, message):
      if not self.bot.ready: return
      if message.author.bot: return # ignore bots for now

      # moon phase
      if "moon" in self.bot.tokenize(message.clean_content):
         moon_phase = get_moon_emoji()
         if moon_phase is not None:
            await asyncio.sleep(random.uniform(1,2))
            await message.add_reaction(moon_phase)

   @commands.command()
   async def moon(self, ctx):
      """Gives a little summary of the current lunar phase"""
      summary = get_moon_summary()
      await self.bot.type_(ctx.channel, summary)
      msg = await ctx.send(summary)

   @tasks.loop(minutes=97)
   async def check_moon_phase(self):
      channel_id = remember(self.bot.memory, "MOON_UPDATES")
      if channel_id is not None:
         mi = get_moon_info()
         if mi.phase_name != self.bot.last_moon_info.phase_name:
            self.bot.last_moon_info = mi
            channel = self.bot.get_channel(int(channel_id))
            await channel.send(get_moon_summary())

def setup(bot):
   bot.add_cog(Lunar(bot))
