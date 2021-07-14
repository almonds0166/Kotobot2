
import random
import asyncio

from discord.ext import commands, tasks

import sys; sys.path.append("..")
from util import remember

class DadCog(commands.Cog):
   """Behavior that has to do with making "Hi X, I'm Dad" jokes.
   """
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_message(self, message):
      if not self.bot.ready: return
      if message.author.bot: return # ignore bots for now

      # detect potential for dad jokes
      first_line = message.clean_content.split("\n")[0]
      name = self.bot.rex.hi_im_dad(first_line)
      if name and name.lower() not in ("dad"):
         if len(name) <= 32:
            await asyncio.sleep(random.uniform(1,2))
            smirk = remember(self.bot.memory, "SMIRK_EMOJI", default="😏")
            await message.add_reaction(smirk)
            if False: #random.uniform(0, 70) > len(name):
               content = f"Hi {name}, I'm Dad"
               await self.bot.type_(message.channel, content)
               ref = message.to_reference()
               await message.channel.send(
                  content,
                  reference=ref,
                  mention_author=False
               )
         else:
            pass # eh, if it's too long, don't bother

def setup(bot):
   bot.add_cog(DadCog(bot))