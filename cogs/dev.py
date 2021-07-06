
from discord.ext import commands, tasks

import sys; sys.path.append("..")
from util import remember, forget

class DeveloperCog(commands.Cog):
   """Commands only the bot developer can use.
   """
   def __init__(self, bot):
      self.bot = bot

   @commands.command()
   @commands.is_owner()
   async def tokenize(self, ctx, *, args=""):
      if not args: return
      tokens = self.bot.tokenize(args)
      await ctx.send(str(tokens))

   @commands.command()
   @commands.is_owner()
   async def reload(self, ctx, *modules):
      if len(modules) == 0:
         modules = self.bot.available_modules()

      for module in modules:
         print(f"Reloading cogs.{module}... ", end="")
         self.bot.reload_extension(f"cogs.{module}")
         print("done.")

      await ctx.send(
         f"Reloaded the following extensions: " + \
         ", ".join(f"`{module}`" for module in modules)
      )

   @commands.command()
   @commands.is_owner()
   async def remember(self, ctx, key: str, value: str=None):
      if value is None:
         item = remember(self.bot.memory, key)
         if item is None:
            await ctx.send(f"No value saved for key `{key}` yet")
         else:
            await ctx.send(f"`{key}: {item}`")
      else:
         remember(self.bot.memory, key, value)
         await ctx.message.add_reaction("👌")

   @commands.command()
   @commands.is_owner()
   async def forget(self, ctx, key: str):
      forget(self.bot.memory, key)
      await ctx.message.add_reaction("👌")



def setup(bot):
   bot.add_cog(DeveloperCog(bot))