
from collections import namedtuple

from discord.ext import commands

VersionInfo = namedtuple("VersionInfo", "major minor build")

version_info = VersionInfo(
   major=2,
   minor=0,
   build=85,
)

__version__ = f"{version_info.major}.{version_info.minor:02d}.{version_info.build:04d}"

class VersionCog(commands.Cog):
   """Handles version info"""
   def __init__(self, bot):
      self.bot = bot
      self.bot.version_info = version_info
      self.bot.__version__ = __version__

def setup(bot):
   bot.add_cog(VersionCog(bot))