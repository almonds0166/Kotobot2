
import os
import codecs
from http.client import responses as RESPONSE_CODES
import asyncio

import aiohttp
import discord
from discord.ext import commands

class Main(commands.Cog):
   """General commands"""
   def __init__(self, bot):
      self.bot = bot

   @commands.command()
   async def rot13(self, ctx, *, args=None):
      """The best cryptographic cipher"""
      if args is None: return
      await ctx.send(codecs.encode(args, "rot_13"))

   @commands.command(aliases=["dogs", "doggo"])
   async def dog(self, ctx):
      """Random doggo"""
      headers = self.bot.headers.copy()
      api_key = os.getenv("THE_DOG_API_KEY")
      if api_key: headers["x-api-key"] = api_key
      async with aiohttp.ClientSession(headers=self.bot.headers) as session:
         async with session.get("https://api.thedogapi.com/v1/images/search") as response:
            code = response.status
            if code != 200:
               await ctx.send(f"Received `{code} {RESPONSE_CODES[code]}` 😦")
               return
            r = (await response.json())[0]

         has_info = bool(r["breeds"])

         e = discord.Embed(
            title="Random doggo" if not has_info else r["breeds"][0]["name"],
            #description=r[""],
            color=self.bot.color,
         )
         if has_info:
            weight_m = r["breeds"][0]["weight"]["metric"].replace(" - ", "–") + " kg"
            weight_i = r["breeds"][0]["weight"]["imperial"].replace(" - ", "–") + " lbs"
            height_m = r["breeds"][0]["height"]["metric"].replace(" - ", "–") + " cm"
            height_i = r["breeds"][0]["height"]["imperial"].replace(" - ", "–") + " in"
            e.add_field(
               name="Height",
               value=f"{height_m} ({height_i})",
               inline=True
            )
            e.add_field(
               name="Weight",
               value=f"{weight_m} ({weight_i})",
               inline=True
            )
            e.add_field(
               name="Life span",
               value=r["breeds"][0]["life_span"].replace(" - ", "–"),
               inline=True
            )
            e.add_field(
               name="Bred for",
               value=r["breeds"][0]["bred_for"],
               inline=False
            )
            e.add_field(
               name="Temperament",
               value=r["breeds"][0]["temperament"],
               inline=False
            )

         e.set_image(url=r["url"])

         await ctx.send(embed=e)

def setup(bot):
   bot.add_cog(Main(bot))