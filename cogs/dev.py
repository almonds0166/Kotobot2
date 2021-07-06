
from discord.ext import commands, tasks

class DeveloperCog(commands.Cog):
   """Commands only the bot developer can use.
   """
   def __init__(self, bot):
      self.bot = bot

   @commands.command()
   @commands.is_owner()
   async def tokenize(self, ctx, *, args=""):
      if not args: return
      tokens = self.bot.tokenizer.encode(args).tokens
      await ctx.send(str(tokens))

   @commands.command()
   @commands.is_owner()
   async def reload(self, ctx, *modules):
      if len(modules) == 0:
         modules = []
         for file in (self.bot.path / "cogs").iterdir():
            if file.suffix != ".py": continue
            modules.append(file.stem)
            print(f"Reloading cogs.{file.stem}... ", end="")
            self.bot.reload_extension(f"cogs.{file.stem}")
            print("done.")
      else:
         for module in modules:
            print(f"Reloading cogs.{module}... ", end="")
            self.bot.reload_extension(f"cogs.{module}")
            print("done.")
      await ctx.send(
         f"Reloaded the following extensions: " + \
         ", ".join(f"`{module}`" for module in modules)
      )


def setup(bot):
   bot.add_cog(DeveloperCog(bot))