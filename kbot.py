
import os
from pathlib import Path
import random
import datetime
from typing import List

import asyncio
import discord
from discord.ext import commands, tasks
import asyncpraw
from asyncprawcore import NotFound
import tokenizers

from util import Rex, get_moon_emoji, get_moon_info

class Kotobot(commands.Bot):
   def __init__(self):
      super().__init__(
         "$",
         case_insensitive=True,
         help_command=None,
      )

      self.headers = {
         "User-Agent": "Kotobot/2.0",
      }
      self.rex = Rex()
      self.reddit = asyncpraw.Reddit(
         client_id=os.environ["KBOT_REDDIT_CLIENT_ID"],
         client_secret=os.environ["KBOT_REDDIT_CLIENT_SECRET"],
         user_agent=self.headers["User-Agent"]
      )
      self.last_moon_info = get_moon_info()

      self.color = discord.Colour(16747354) # https://www.spycolor.com/

      self.normalizer = tokenizers.normalizers.BertNormalizer()
      self.pre_tokenizer = tokenizers.pre_tokenizers.BertPreTokenizer()
      
      self.path = Path(__file__).parent
      self.loaded_modules = set()
      for module in self.available_modules():
         print(f"Loading cogs.{module}... ", end="")
         self.load_extension(f"cogs.{module}")
         print("done.")
         self.loaded_modules.add(module)

      self.memory = Path("./koto.ltm")

      self.t0 = datetime.datetime.utcnow()
      self.disconnects = 0
      self.ready = False

   @property
   def uptime(self) -> datetime.timedelta:
      return datetime.datetime.utcnow() - self.t0

   def format_uptime(self) -> str:
      seconds = int(self.uptime.total_seconds())
      minutes = seconds // 60
      hours = minutes // 60
      days = hours // 24
      if days:
         return f"{days}d{hours%24:02d}h{minutes%60:02d}m"
      else:
         return f"{hours}h{minutes%60:02d}m{seconds%60:02d}s"

   def available_modules(self):
      modules = set()
      for file in (self.path / "cogs").iterdir():
         if file.suffix != ".py": continue
         modules.add(file.stem)
      return modules

   def tokenize(self, sequence: str) -> List[str]:
      """Break up a sequence of words into word-level tokens.
      """
      normalized = self.normalizer.normalize_str(sequence)
      tokenized = self.pre_tokenizer.pre_tokenize_str(normalized)
      return [word for word, _ in tokenized]

   async def type_(self, channel, msg: str):
      cps = random.triangular(8,12,9) # characters per second
      await asyncio.sleep(random.uniform(0.5,1))
      async with channel.typing():
         await asyncio.sleep(len(msg) / cps)

   async def on_ready(self):
      if not self.ready:
         self.t0 = datetime.datetime.utcnow()
         print("Logged in.")
      else:
         self.disconnects += 1
         print("Re-established Discord connection.")

      self.ready = True

if __name__ == "__main__":
   kbot = Kotobot()
   kbot.run(os.environ["KBOT_TOKEN"])
