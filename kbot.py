
import os
from pathlib import Path
import random
from typing import List

import asyncio
import discord
from discord.ext import commands, tasks
import asyncpraw
from asyncprawcore import NotFound
import tokenizers

from util import Rex

class Kotobot(commands.Bot):
   def __init__(self):
      super().__init__(
         "$",
         #case_insensitive=True,
         #help_command=None,
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

      self.color = discord.Colour(16747354) # https://www.spycolor.com/

      self.tokenizer = tokenizers.Tokenizer(tokenizers.models.BPE(unk_token="[UNK]"))
      self.tokenizer.normalizer = tokenizers.normalizers.BertNormalizer()
      self.tokenizer.pre_tokenizer = tokenizers.pre_tokenizers.BertPreTokenizer()
      
      self.path = Path(__file__).parent
      for file in (self.path / "cogs").iterdir():
         if file.suffix != ".py": continue
         print(f"Loading cogs.{file.stem}... ", end="")
         self.load_extension(f"cogs.{file.stem}")
         print("done.")

      self.disconnects = 0
      self.ready = False

   async def on_ready(self):
      if not self.ready:
         print("Logged in.")
      else:
         self.disconnects += 1
         print("Re-established Discord connection.")

      self.ready = True

if __name__ == "__main__":
   kbot = Kotobot()
   kbot.run(os.environ["KBOT_TOKEN"])
