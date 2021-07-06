
import discord
from discord.ext import commands, tasks
import git

import sys; sys.path.append("..")
from util import remember, forget, inflect_number

class Developer(commands.Cog):
   """Commands only the bot developer can use"""
   def __init__(self, bot):
      self.bot = bot

   @commands.command()
   @commands.is_owner()
   async def tokenize(self, ctx, *, args=""):
      """Test out the tokenizer on an input sequence"""
      if not args: return
      tokens = self.bot.tokenize(args)
      await ctx.send(str(tokens))

   @commands.command()
   @commands.is_owner()
   async def reload(self, ctx, *modules):
      """Reload some or all extensions."""
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
      """Lookup or set a value in long-term memory"""
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
      """Forget a value in long-term memory"""
      forget(self.bot.memory, key)
      await ctx.message.add_reaction("👌")

   @commands.group(
      invoke_without_command=True,
      description="``git version``, ``git status``, and ``git pull`` supported"
   )
   @commands.is_owner()
   async def git(self, ctx):
      """git functionality"""
      pass

   @git.command()
   async def version(self, ctx):
      await ctx.send(f"GitPython=={git.__version__}")

   @git.command()
   async def status(self, ctx):
      e = discord.Embed(
         title="git status",
         description="",
         color=self.bot.color,
      )
      repo = git.Repo(self.bot.path)

      if not repo.is_dirty():
         e.description = "Repo is clean!"
         await ctx.send(embed=e)
         return

      # status on changed files
      changed_files = []
      for item in repo.index.diff(None):
         changed_files.append(item.a_path)

      changes = len(changed_files)
      if changes > 10:
         changed_files = changed_files[:5]
         changed_files.append("...")

      if changes:
         changes_ = inflect_number("change", changes)
         e.add_field(
            name=f"{changes} {changes_}",
            value="\n".join(f"`{file}`" for file in changed_files),
            inline=True
         )

      # status on untracked files
      untracked_files = repo.untracked_files
      num_files = len(untracked_files)
      if num_files > 10:
         untracked_files = untracked_files[:5]
         untracked_files.append("...")

      if num_files:
         files = inflect_number("file", num_files)
         e.add_field(
            name=f"{num_files} untracked {files}",
            value="\n".join(f"`{file}`" for file in untracked_files),
            inline=True
         )

      await ctx.send(embed=e)

   @git.command()
   async def pull(self, ctx):
      repo = git.Repo(self.bot.path)
      o = repo.remotes.origin
      fetch_infos = o.pull()
      await ctx.send((
         f"Done.\n"
         f"{len(fetch_infos)=}\n"
         f"Remember to reload any updated extensions."
      ))

def setup(bot):
   bot.add_cog(Developer(bot))