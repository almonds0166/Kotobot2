
import discord
from discord.ext import commands

PREFIX = "$"
BOT_NAME = "Kotobot"
BOTTOM_INFO = ""

class Meta(commands.Cog):
   """Meta cog"""
   def __init__(self, bot):
      self.bot = bot

   @commands.command()
   async def stats(self, ctx):
      """Gives some analytics"""
      description = (
         f"{BOT_NAME} v{self.bot.__version__} "
         f"([source](https://github.com/almonds0166/Kotobot2))"
      )

      e = discord.Embed(
         title="Info",
         description=description,
         color=self.bot.color,
      )
      e.add_field(
         name="Uptime",
         value=f"{self.bot.format_uptime()} ({self.bot.disconnects} disconnects)",
         inline=True
      )

      await ctx.send(embed=e)

   # Credit: https://github.com/zedchance/embed_help
   @commands.command(name="help")
   async def help_command(self, ctx, *commands: str):
      """Shares bot help information"""
      bot = ctx.bot
      embed = discord.Embed(
         title=f"Kotobot v{bot.__version__}",
         description="",
         color=self.bot.color,
      )

      def generate_usage(command_name):
         """Generates a string of how to use a command"""
         temp = f"{PREFIX}"
         command = bot.get_command(command_name)
         # Aliases
         if len(command.aliases) == 0:
            temp += f"{command_name}"
         elif len(command.aliases) == 1:
            temp += f"[{command.name}|{command.aliases[0]}]"
         else:
            t = "|".join(command.aliases)
            temp += f"[{command.name}|{t}]"
         # Parameters
         params = f" "
         for param in command.clean_params:
            params += f"<{command.clean_params[param]}> "
         temp += f"{params}"
         return temp

      def generate_command_list(cog):
         """Generates the command list with properly spaced help messages"""
         # Determine longest word
         max = 0
         for command in bot.get_cog(cog).get_commands():
            if not command.hidden:
               if len(f"{command}") > max:
                  max = len(f"{command}")
         # Build list
         temp = ""
         for command in bot.get_cog(cog).get_commands():
            if command.hidden:
               temp += ""
            elif command.help is None:
               temp += f"{command}\n"
            else:
               temp += f"`{command}`"
               for i in range(0, max - len(f"{command}") + 1):
                  temp += "   "
               temp += f"{command.help}\n"
         return temp

      # Help by itself just lists our own commands.
      if len(commands) == 0:
         for cog in bot.cogs:
            temp = generate_command_list(cog)
            if temp != "":
               embed.add_field(name=f"**{cog}**", value=temp, inline=False)
         if BOTTOM_INFO != "":
            embed.add_field(name="Info", value=BOTTOM_INFO, inline=False)
      elif len(commands) == 1:
         # Try to see if it is a cog name
         name = commands[0]
         command = None

         if name in bot.cogs:
            cog = bot.get_cog(name)
            msg = generate_command_list(name)
            embed.add_field(name=name, value=msg, inline=False)
            msg = f"{cog.description}\n"
            embed.set_footer(text=msg)

         # Must be a command then
         else:
            command = bot.get_command(name)
            if command is not None:
               help = f""
               if command.help is not None:
                  help = command.help
               embed.add_field(name=f"**{command}**",
                           value=f"{command.description}```{generate_usage(name)}```\n{help}",
                           inline=False)
            else:
               msg = " ".join(commands)
               embed.add_field(name="Not found", value=f"Command/category `{msg}` not found.")
      else:
         msg = " ".join(commands)
         embed.add_field(name="Not found", value=f"Command/category `{msg}` not found.")

      await ctx.send("", embed=embed)
      return

def setup(bot):
   bot.add_cog(Meta(bot))