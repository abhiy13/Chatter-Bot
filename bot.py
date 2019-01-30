import discord
from pymongo import MongoClient
from pprint import pprint
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import math
import sys
sys.path.insert(0, './rating_fetch/')
sys.path.insert(0, './db/')
import cc, cf, hr, createuser, update
from kepp_alive import keep_alive

Client = discord.Client() 
client = commands.Bot(command_prefix = "!")

MongoURI = 'mongodb://abhishek:abhishek1@ds247290.mlab.com:47290/chatter_bot_db'
clientt = MongoClient(MongoURI)
db = clientt['chatter_bot_db'] 

users = db['users']

@client.event
async def on_ready():
  await client.change_presence(game=discord.Game(name='Algo and Ds'))
  print("Bot is Now Online")

@client.event
async def on_message(message):
  ar = message.content.split()
  id = message.author.id
  server = client.get_server(id="512977453061242899")
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
  
  if ar[0].upper() == "!SETHANDLE":
    cc, cf = ar[1], ar[2]
    response = createuser.createUser(id, cc, cf)
    await client.send_message(message.channel, response)
    await client.send_message(message.channel, "Query By <@{}>".format(id))
    grandmaster = []
    master = []
    expert = []
    unassigned = []
    find = users.find().sort('rating', -1)
    for use in find:
      if len(grandmaster) < 1:
        grandmaster.append(use['discord'])
        continue
      if len(master) < 2:
        master.append(use['discord'])
        continue
      if len(expert) < 5:
        expert.append(use['discord'])
        continue
    Grandmaster = []
    Master = []
    Expert = []
    Unassigned = []
    for i in server.members:
      Unassigned.append(i)
      if i.id in grandmaster:
        Grandmaster.append(i)
        continue
      if i.id in master:
        Master.append(i)
        continue
      if i.id in expert:
        Expert.append(i)
        continue
    role = discord.utils.get(server.roles, name = 'unassigned')
    for member in server.members:
      rem = []
      if "admin" in member.roles:
        continue
      if "Bot" in member.roles:
        continue 
      if len(member.roles) == 0:
        unassigned.append(member)
      for i in member.roles:
        j = i
        print(j, end = ' ')
        if j != "@everyone" and j != "admin":
          rem.append(j)
      try:
        await client.remove_roles(member, *rem)
      except:
        print("SHIT")
      role = discord.utils.get(server.roles, name = 'Grandmaster')
      for member in Grandmaster:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Master')  
      for member in Master:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Expert')
      for member in Expert:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'unassigned')
      for member in Unassigned:
        await client.add_roles(member, role) 

  
  if ar[0].upper() == "!GETRATING":
    find = users.find_one({'discord': id})
    response = "Your Codechef Handle : **{0}** and Codeforces Handle : **{1}** has a rating of **{2}**".format(find['codechef'], find['codeforces'], find['rating'])
    await client.send_message(message.channel, response)
    await client.send_message(message.channel, "Query By <@{}>".format(id))

  if ar[0].upper() == "!UPDATEROLES":
    grandmaster = []
    master = []
    expert = []
    unassigned = []
    find = users.find().sort('rating', -1)
    for use in find:
      if len(grandmaster) < 1:
        grandmaster.append(use['discord'])
        continue
      if len(master) < 2:
        master.append(use['discord'])
        continue
      if len(expert) < 5:
        expert.append(use['discord'])
        continue
    Grandmaster = []
    Master = []
    Expert = []
    Unassigned = []
    for i in server.members:
      Unassigned.append(i)
      if i.id in grandmaster:
        Grandmaster.append(i)
        continue
      if i.id in master:
        Master.append(i)
        continue
      if i.id in expert:
        Expert.append(i)
        continue
    role = discord.utils.get(server.roles, name = 'unassigned')
    for member in server.members:
      rem = []
      if "admin" in member.roles:
        continue
      if "Bot" in member.roles:
        continue 
      if len(member.roles) == 0:
        unassigned.append(member)
      for i in member.roles:
        j = i
        print(j, end = ' ')
        if j != "@everyone" and j != "admin":
          rem.append(j)
      try:
        await client.remove_roles(member, *rem)
      except:
        print("SHIT")

      role = discord.utils.get(server.roles, name = 'Grandmaster')
      for member in Grandmaster:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Master')  
      for member in Master:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Expert')
      for member in Expert:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'unassigned')
      for member in Unassigned:
        await client.add_roles(member, role) 

    
        
keep_alive()
client.run("NTM1NDQ5NDI5ODY0NjExODQw.DzMRqA.9ROgoqNKXnS7fhwRDyb3ak-jGBM")