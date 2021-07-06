
import sys
import traceback

from discord.ext import commands

# ignore these errors
IGNORE = (
   commands.CommandNotFound,
   commands.MissingRequiredArgument,
   commands.DisabledCommand,
   commands.NoPrivateMessage,
)

class ErrorCog(commands.Cog):
   """This cog handles command errors.

   Credit: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
   """
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_command_error(self, ctx, error):
      # Prevent commands with local handlers being handled here
      if hasattr(ctx.command, "on_error"): return

      # This prevents any cogs with an overwritten cog_command_error being handled here.
      cog = ctx.cog
      if cog and cog._get_overridden_method(cog.cog_command_error) is not None: return

      # Allows us to check for original exceptions raised and sent to CommandInvokeError.
      # If nothing is found. We keep the exception passed to on_command_error.
      error = getattr(error, "original", error)

      if isinstance(error, IGNORE): return

      if isinstance(error, commands.BadArgument):
         await ctx.send("Bad argument for `{self.bot.command_prefix}{ctx.command.qualified_name}`")
         return

      # All other Errors not returned come here. And we can just print the default TraceBack.
      print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
      traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
   bot.add_cog(ErrorCog(bot))