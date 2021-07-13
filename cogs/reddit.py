
import discord
from discord.ext import commands, tasks

import sys; sys.path.append("..")
from util import shorten_title

class RedditCog(commands.Cog):
   """Behavior that has to do with detecting subreddits in users' messages.
   """
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_message(self, message):
      if not self.bot.ready: return
      if message.author.bot: return # ignore bots for now

      # detect subreddits
      potential_subreddits = self.bot.rex.subreddits(message.content)
      if potential_subreddits:
         async with message.channel.typing():
            subreddits = [] # we check if they're legit subreddits
            for sr in potential_subreddits:
               try:
                  async for _ in self.bot.reddit.subreddits.search_by_name(sr, exact=True):
                     pass
               except NotFound:
                  pass
               else:
                  subreddits.append(sr)
            if subreddits:
               embed = discord.Embed(colour=self.bot.color)
               name = "Mentioned subreddits"
               value = ""
               if len(subreddits) == 1:
                  sr = subreddits[0]
                  embed.title = f"r/{sr}"
                  embed.url = f"https://reddit.com/r/{sr}/"
                  subreddit = await self.bot.reddit.subreddit(sr)
                  submissions = []
                  for time_filter in ("day", "week", "month", "year", "all"):
                     async for submission in subreddit.top(time_filter=time_filter, limit=5):
                        title = shorten_title(submission.title, max_length=48)
                        # escape some markdown
                        title = title.replace("\\", "\\\\")
                        title = title.replace("[", "\\[")
                        title = title.replace("]", "\\]")
                        title = title.replace("_", "\\_")
                        link = f"https://reddit.com{submission.permalink}"
                        nsfw = submission.over_18
                        pinned = submission.stickied
                        score = submission.score
                        score = f"⬆️ {score}" if score >= 0 else f"⬇️ {-score}"
                        prefix = f"{'⚠️' if nsfw else ''}{'📌' if pinned else ''}"
                        if len(prefix): prefix += " "
                        submissions.append(f"\\* \\[[{score}]({link})\\] {prefix}{title}")
                     if len(submissions) >= 3: # ideally between 3 and 5 posts
                        break
                     elif time_filter != "all":
                        submissions = []
                  if time_filter == "all":
                     name = "Top posts from all time"
                  else:
                     name = f"Top posts from the past {time_filter}"
                  if submissions:
                     value = "\n".join(submissions)
                  else:
                     value = "There're no submissions in this subreddit yet."
               else:
                  bullet_list = [f"\\* [r/{sr}](https://reddit.com/r/{sr}/)" for sr in subreddits]
                  if len(subreddits) > 16:
                     value = "\n".join(bullet_list[:15]) + "\n..."
                  elif len(subreddits) > 1:
                     value = "\n".join(bullet_list)
               embed.add_field(name=name, value=value, inline=False)
               ref = message.to_reference()
               await message.channel.send(
                  "",
                  embed=embed,
                  reference=ref,
                  mention_author=False
               )
            else:
               await message.add_reaction("🤔")

def setup(bot):
   bot.add_cog(RedditCog(bot))
