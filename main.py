# imports

import disnake
import asyncio
import os
import json
import requests
import time

from disnake.ext import commands
from grindzserver import rungrindz
from mee6_py_api import API

# bot

rungrindz()

activity = disnake.Activity(type=disnake.ActivityType.listening, name="XP go brrrrr")
grindz = commands.InteractionBot(activity=activity)

mee6API = API(452237221840551938)

@grindz.slash_command(name="lifesupport", description="Check if the bot is alive.", guild_ids=[1048780081713123338])
async def lifesupport(ctx):
  await ctx.send("I'm alive! :blue_heart:")

@grindz.slash_command(name="info", description="Get an summary of a user's MEE6 information.", guild_ids=[1048780081713123338])
async def info(ctx, user: disnake.User=None):
  if not user:
    user = ctx.author
  data = await mee6API.levels.get_user_details(user.id)
  lvl = data["level"]
  msgcount = data["message_count"]
  xp = data["xp"]
  avrgxppm = xp/msgcount
  avrgxppmr = round(avrgxppm, 1)
  detailedxp = data["detailed_xp"]
  xptonextlvl = int(detailedxp[1]) - int(detailedxp[0])
  nextlvl = lvl + 1

  messagesneed = round(xptonextlvl/20)
  hoursneed = round(messagesneed//60)
  minsneed = round(messagesneed % 60)

  currenttime = round(int(time.time()))
  unixleft = currenttime + (messagesneed*60)
  
  infoembed = disnake.Embed(title=f"MEE6 Information for {user.name}#{user.discriminator}", color=0x00c3e3)
  infoembed.add_field(name="Level", value=lvl, inline=True)
  infoembed.add_field(name="Message Count", value=msgcount, inline=True)
  infoembed.add_field(name="Total XP", value=xp, inline=True)
  infoembed.add_field(name="Average XP Per Message", value=avrgxppmr, inline=True)
  infoembed.add_field(name=f"XP To Level {nextlvl}", value=xptonextlvl, inline=True)
  infoembed.add_field(name=f"Earliest Time To Hit Level {nextlvl}", value=f"<t:{unixleft}>", inline=True)
  infoembed.set_footer(text=f"{messagesneed} messages/{hoursneed} hours and {minsneed} minutes are needed to level up to level {nextlvl}.")
  await ctx.send(embed=infoembed)

@grindz.slash_command(name="echo", description="Make the bot say anything you want.", guild_ids=[1048780081713123338])
async def echo(ctx, message):
  await ctx.send("Echoing message...", ephemeral=True)
  await ctx.channel.send(message)

rungrindz()

# dashboard

loop = asyncio.get_event_loop()
# loop.create_task(sukidi.start(os.getenv("token.sukidi")))
loop.create_task(grindz.start(os.getenv("TOKEN")))
loop.run_forever()
