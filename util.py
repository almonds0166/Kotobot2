
import re

class Rex():
   """Helper class to handle regular expressions-related methods.
   
   Initialization compiles regular expression patterns to be used by the methods.

   Attributes:
      exs (dict[str]): Set of raw strings used to compile the patterns.
      patterns (dict[re.Pattern]): Set of regular expression patterns used by the methods.
   """
   def __init__(self):
      self.ex = {}
      self.patterns = {}

      self.ex["subreddits"] = r"(\s/?|^/?)r/([a-zA-Z0-9_]{3,21})/?(\s|$|[,.!?])"

      for k, v in self.ex.items():
         self.patterns[k] = re.compile(v)

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

if __name__ == "__main__":
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