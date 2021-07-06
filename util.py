
import re
from datetime import datetime
import asyncio

import pylunar

MOON_EMOJIS = {
   "NEW_MOON": "🌑",
   "WAXING_CRESCENT": "🌒",
   "FIRST_QUARTER": "🌓",
   "WAXING_GIBBOUS": "🌔",
   "FULL_MOON": "🌕",
   "WANING_GIBBOUS": "🌖",
   "LAST_QUARTER": "🌗",
   "WANING_CRESCENT": "🌘",
}

class Rex():
   """Helper class to handle regular expressions-related methods.
   
   Initialization compiles regular expression patterns to be used by the methods.

   Attributes:
      exs (dict[str]): Set of raw strings used to compile the patterns.
      patterns (dict[re.Pattern]): Set of regular expression patterns used by the methods.
   """
   def __init__(self):
      self.exs = {}
      self.patterns = {}

      self.exs["subreddits"] = r"(\s/?|^/?)r/([a-zA-Z0-9_]{3,21})/?(\s|$|[,.!?])"
      self.exs["dadjoke"] = r"(^|[.!?:;]\s)((ok|okay|now|and|anyway|so|thus|even),?\s)?(I'm|im|I\sam)\s((\w|\s)+)([,.!:;]|$|\n)"

      for k, v in self.exs.items():
         self.patterns[k] = re.compile(v, re.IGNORECASE)

   def subreddits(self, msg: str):
      """Extract a list of subreddits mentioned within ``msg``.
      
      Parses ``msg`` for any subreddits of the form ``r/subreddit`` or ``/r/subreddit``, returning
      a list of strings. Subreddits don't repeat and are returned in the same order as they appear
      in the input message.

      Args:
         msg: Message potentially containing subreddits.
      """
      seen = set()
      subreddits = []
      for match in self.patterns["subreddits"].finditer(msg):
         sr = match.group(2)
         if sr.lower() not in seen:
            seen.add(sr.lower())
            subreddits.append(sr)
      return subreddits

   def hi_im_dad(self, msg: str):
      """Detects potential for those lovely "Hi X, I'm Dad" jokes.

      For example, an input of "I'm hungry" should return "hungry", because any keen Dad can reply
      with "Hi hungry, I'm Dad." Also picks up "im hungry" and "I am hungry". If no potential for a
      dad joke is found, returns None.

      Args:
         msg: Message to parse.
      """
      for match in self.patterns["dadjoke"].finditer(msg):
         name = match.group(5)
         return name # just pick the first one
      return None

def get_moon_phase() -> str:
   """Returns an emoji representing the current moon phase.
   """

   mi = pylunar.MoonInfo((42, 21, 30), (-71, 3, 35)) # Boston, MA
   mi.update((datetime.utcnow()))
   phase = mi.phase_name()

   return MOON_EMOJIS[phase]

def shorten_title(title: str, max_length: int=32) -> str:
   """Shortens the given string on a word-by-word basis.

   Args:
      title: Title to be shortened if necessary.
      max_length: Max number of characters that the title should have.
   """
   assert max_length >= 3, f"Dude, the max_length you gave me ({max_length}) is way too short."
   # title length is OK
   if len(title) <= max_length:
      return title

   # if the first word is too long
   split_title = title.split(" ")
   if len(split_title[0]) > max_length:
      return split_title[0][:max_length-3] + "..."

   # otherwise, go by words
   short_title = split_title[0]
   for word in split_title[1:]:
      if len(short_title) + len(word) + 1 > max_length-3:
         return short_title + "..."
      short_title += " " + word

# tests for this module

def _subreddits_tests():
   rex = Rex()
   tests = (
      "Hello, this is a test.\n"
      "Hello, this is a test with a r/subreddit in there.\n"
      "Should also detect /r/subreddits\n"
      "But it shouldn't detectr/this case\n"
      "Or detect/r/this case\n"
      "Neither should it detect r/this/case\n"
      "But it should detect this r/case.\n"
      "And importantly, I don't want it to detect reddit.com/r/something like that\n"
   ).strip()
   for test in tests.split("\n"):
      print(test)
      print(f"\t{rex.subreddits(test)}")
   print("")

def _dadjoke_tests():
   rex = Rex()
   tests = (
      "I'm hungry\n"
      "I'm testing this with multiple words\n"
      "I'm going to try this since maybe I want to have a limit to how long this can get\n"
      "I'm wanting to stop at commas, like this.\n"
      "I'm also wanting it to stop at periods.\n"
      "It would be cool if split by sentences. I'm testing.\n"
      "But it shouldn't pick up if I'm starting over here, because it could be conditional.\n"
      "And here, I'm thinking it shouldn't work.\n"
      "And here. I'm thinking it shouldn't work? because of the question mark.\n"
      "Anyway I'm thinking of picking this up.\n"
      "OK, I'm wanting to pick this up, too.\n"
   ).strip()
   for test in tests.split("\n"):
      print(test)
      print(f"\t{rex.hi_im_dad(test)}")
   print("")

def _get_moon_phase():
   loop = asyncio.get_event_loop()
   emoji = loop.run_until_complete(get_moon_phase({"User-Agent": "Kotobot/2.0"}))
   print(emoji)

if __name__ == "__main__":
   _subreddits_tests()
   _dadjoke_tests()
   _get_moon_phase()