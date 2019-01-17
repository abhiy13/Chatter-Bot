import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import math
import sys
sys.path.insert(0, './rating_fetch/')
import cc, cf, hr

Client = discord.Client() 
client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
  print("Bot is Now Online")

@client.event
async def on_message(message):
  ar = message.content.split()
  id = message.author.id
  if(ar[0].upper() == "!CC"):
    x = cc.get_rating(ar[1])
    await client.send_message(message.channel, x)
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  if(ar[0].upper() == "!HR"):
    x = hr.get_rating(ar[1])
    await client.send_message(message.channel, x)
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  if(ar[0].upper() == "!CF"):
    x = cf.get_rating(ar[1])
    await client.send_message(message.channel, x)
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  if(ar[0].upper() == "!POW"):
    if(len(ar) < 3):
      await client.send_message(message.channel, "Insuffecient Args")
      await client.send_message(message.channel, "Query By <@{}>".format(id))
    await client.send_message(message.channel, (int)(int(ar[1]) ** int(ar[2])))
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  if(ar[0].upper() == "!FACT"):
    await client.send_message(message.channel, math.factorial(int(ar[1]))) 
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  if(ar[0].upper() == "!MUL"):
    ans = 1
    first = 0
    for i in ar:
      if first == 0:
        first = 1
        continue
      ans *= int(i)
    await client.send_message(message.channel, ans)
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  if(ar[0].upper() == "!REPEAT"):
    ar = ar[1:]
    await client.send_message(message.channel, " ".join(ar))
    await client.send_message(message.channel, "Query By <@{}>".format(id))  
  
  if(ar[0].upper() == "!SOME_ADMIN_COMMAND"):
    if "512990178315468803" in [role.id for role in message.author.roles]:
      await client.send_message(message.channel, "YES you can")
    else:
      await client.send_message(message.channel, "NOPE U can't")
    await client.send_message(message.channel, "Query By <@{}>".format(id))      
      

client.run("NTM1NDQ5NDI5ODY0NjExODQw.DyIWaw.F0KyCrvQfy0HTyvWvQNN3OnlWHI")