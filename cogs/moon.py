
from discord.ext import commands, tasks

import sys; sys.path.append("..")
from util import get_moon_phase

class MoonCog(commands.Cog):
   """Behavior that has to do with phases of the moon.
   """
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_message(self, message):
      if not self.bot.ready: return
      if message.author.bot: return # ignore bots for now

      # moon phase
      if "moon" in message.clean_content.lower().split(" "):
         moon_phase = get_moon_phase()
         if moon_phase is not None:
            await asyncio.sleep(random.uniform(1,2))
            await message.add_reaction(moon_phase)

def setup(bot):
   bot.add_cog(MoonCog(bot))
