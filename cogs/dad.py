
import random
import asyncio

from discord.ext import commands, tasks

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
      name = self.bot.rex.hi_im_dad(message.clean_content)
      if name and name.lower() not in ("dad"):
         if len(name) <= 32:
            await asyncio.sleep(random.uniform(1,2))
            await message.add_reaction("😏")
            if True or random.uniform(0, 70) > len(name):
               content = f"Hi {name}, I'm Dad"
               cps = random.triangular(8,12,9) # characters per second
               await asyncio.sleep(random.uniform(0.5,1))
               async with message.channel.typing():
                  await asyncio.sleep(len(content) / cps)
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