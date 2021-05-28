
import os
import random

import asyncio
import discord
import asyncpraw
from asyncprawcore import NotFound

from util import Rex, shorten_title

class Kotobot(discord.Client):
   def __init__(self):
      super().__init__()

      self.rex = Rex()
      self.reddit = asyncpraw.Reddit(
         client_id=os.environ["KBOT_REDDIT_CLIENT_ID"],
         client_secret=os.environ["KBOT_REDDIT_CLIENT_SECRET"],
         user_agent="Kotobot/2.0"
      )

      self.ready = False

   async def on_ready(self):
      if not self.ready:
         print("Logged in.")
      else:
         print("Re-established Discord connection.")
      self.ready = True

   async def on_message(self, message):
      if not self.ready: return
      if message.author.bot: return # ignore bots

      # detect potential for dad jokes
      name = self.rex.hi_im_dad(message.clean_content)
      if name:
         if len(name) <= 32:
            await asyncio.sleep(random.uniform(1,2))
            await message.add_reaction("<:heh:847744125788356608>") # custom emoji
            if random.uniform(0, 70) > len(name):
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

      # detect subreddits
      potential_subreddits = self.rex.subreddits(message.content)
      if potential_subreddits:
         async with message.channel.typing():
            subreddits = [] # we check if they're legit subreddits
            for sr in potential_subreddits:
               try:
                  async for _ in self.reddit.subreddits.search_by_name(sr, exact=True):
                     pass
               except NotFound:
                  pass
               else:
                  subreddits.append(sr)
            if subreddits:
               content = ""
               embed = discord.Embed()
               embed.title = "Mentioned subreddits"
               embed.description = ""
               if len(subreddits) == 1:
                  sr = subreddits[0]
                  embed.title = f"r/{sr}"
                  embed.url = f"https://reddit.com/r/{sr}/"
                  subreddit = await self.reddit.subreddit(sr)
                  submissions = []
                  for time_filter in ("day", "week", "month", "year", "all"):
                     async for submission in subreddit.top(time_filter=time_filter, limit=5):
                        title = shorten_title(submission.title, max_length=48)
                        link = f"https://reddit.com{submission.permalink}"
                        nsfw = submission.over_18
                        pinned = submission.stickied
                        score = submission.score
                        score = f"⬆️{score}" if score >= 0 else f"⬇️{-score}"
                        prefix = f"{'⚠️' if nsfw else ''}{'📌' if pinned else ''}"
                        if len(prefix): prefix += " "
                        submissions.append(f"* \\[[{score}]({link})\\] {prefix}{title}")
                     if submissions: break
                  if submissions:
                     embed.description = "\n".join(submissions)
                     if time_filter == "all":
                        embed.description = \
                           "Top posts from all time\n" + \
                           embed.description
                     else:
                        embed.description = \
                           f"Top posts from the past {time_filter}\n" + \
                           embed.description
                  else:
                     embed.description = "There're no submissions in this subreddit yet."
               else:
                  bullet_list = [f"* [r/{sr}](https://reddit.com/r/{sr}/)" for sr in subreddits]
                  if len(subreddits) > 16:
                     embed.description = "\n".join(bullet_list[:15]) + "\n..."
                  elif len(subreddits) > 1:
                     embed.description = "\n".join(bullet_list)
               ref = message.to_reference()
               await message.channel.send(
                  content=content,
                  embed=embed,
                  reference=ref,
                  mention_author=False
               )

if __name__ == "__main__":
   kbot = Kotobot()
   kbot.run(os.environ["KBOT_TOKEN"], bot=True)
