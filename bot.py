import discord
from pymongo import MongoClient
from env import Env
from pprint import pprint
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import math
import sys
sys.path.insert(0, './rating_fetch/')
sys.path.insert(0, './db/')
from kepp_alive import keep_alive

Client = discord.Client() 
client = commands.Bot(command_prefix = "!")
env_vals = Env()

MongoURI = env_vals.get_bot_uri()
clientt = MongoClient(MongoURI)
db = clientt['chatter_bot_db'] 

users = db['users']

@client.event
async def on_ready():
  await client.change_presence(game=discord.Game(name='Algo and Ds'))
  print("Bot is Now Online")

@client.event
async def on_message(message):
  import cc, cf, createuser, update
  ar = message.content.split()
  id = message.author.id
  server = client.get_server(id="512977453061242899")
  
  if ar[0].upper() == "!HELP":
    response = "Hey, Bot this Side\nThe bot has been developed by AbhiY13 and you can contribute by heading to the github repository https://github.com/AbhiY98/chatter-Bot\n"
    response1 = "The following are some commands of this bot,\n`!pow a b` returns a^b\n`!mul args..` you can put in multiple arguments and it will multiply the values for you\n"
    response2 = "`!fact x` returns x factorial\n`!cc handle` returns codechef rating for handle\n`!cf handle` returns codeforces rating for handle\n`!sethandle cf_handle cc_handle` registers your codechef and codeforces handles and assigns you a role\n`!MODPOW x y MOD` return (x ^ y) % MOD\n"
    response3 = "`!getrating` to know your rating\n Features like updation and others will be added soon.\nIf you would like to contribute please head over to the Github Repository"
    wts = response + response1 + response2 + response3
    await client.send_message(message.channel, wts)
  
  if(ar[0].upper() == "!CC"):
    x = cc.get_rating(ar[1])
    if(x == -1) :
      await client.send_message(message.channel, "CC ID Not Found")
      await client.send_message(message.channel, "Query By <@{}>".format(id))
    else:
      await client.send_message(message.channel, x)
      await client.send_message(message.channel, "Query By <@{}>".format(id))

  '''
  if(ar[0].upper() == "!HR"):
    x = hr.get_rating(ar[1])
    await client.send_message(message.channel, x)
    await client.send_message(message.channel, "Query By <@{}>".format(id))
  '''

  if(ar[0].upper() == "!CF"):
    x = cf.get_rating(ar[1])
    if x == -1:
      await client.send_message(message.channel, "CF ID Not Found")      
    else:
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
  
  if(ar[0].upper() == "!MODPOW"):
    x = int(ar[1]) 
    p = int(ar[2])
    MOD = int(ar[3])
    ans = 1
    while p > 0:
      if (p % 2) == 1:
        ans = (ans * x) % MOD
      x = (x * x) % MOD
      p >>= 1
    await client.send_message(message.channel, ans) 
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
      ll = [str(x).upper() for x in i.roles]
      if "BOT" in ll:
        continue
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
      ll = [str(x).upper() for x in member.roles]
      if "BOT" in ll:
        continue
      for i in member.roles:
        if str(i) != "admin":
          rem.append(i)
      try:
        await client.remove_roles(member, *rem)
      except:
        print("SHIT")

      role = discord.utils.get(server.roles, name = 'Grandmaster')
      for member in Grandmaster:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Master')  
      for member in Master:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Expert')
      for member in Expert:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'unassigned')
      for member in Unassigned:
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role) 

  
  if ar[0].upper() == "!GETRATING":
    findc = users.find({'discord': id}).count()
    if findc == 0:
      await client.send_message(message.channel, "You Do Not Posess An Account Yet !")
      await client.send_message(message.channel, "Query By <@{}>".format(id))
    else:
      find = users.find_one({'discord': id})
      response = "Your Codechef Handle : **{0}** and Codeforces Handle : **{1}** has a rating of **{2}**".format(find['codechef'], find['codeforces'], find['rating'])
      await client.send_message(message.channel, response)
      await client.send_message(message.channel, "Query By <@{}>".format(id))

  if ar[0].upper() == "!TEST":
    for member in server.members:
      print(member.name, *member.roles, end = ' ')
      ll = [str(x).upper() for x in member.roles]
      if "BOT" in ll:
        print("YES BOT", end = ' ')
      print("")

  if ar[0].upper() == "!UPDATEROLES":
    if "496366601470345252" != str(message.author.id):
      await client.send_message(message.channel, "You Do Not Have Admin Privilleges !")
      return
    await client.send_message(message.channel, "Updating The Ratings, This Might Take a While !")
    await client.send_message(message.channel, "Query By <@{}>".format(id))
    grandmaster = []
    master = []
    expert = []
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
      ll = [str(x).upper() for x in i.roles]
      if "BOT" in ll:
        continue
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
      ll = [str(x).upper() for x in member.roles]
      if "BOT" in ll:
        continue
      for i in member.roles:
        if str(i) != "admin":
          rem.append(i)
      try:
        await client.remove_roles(member, *rem)
      except:
        print("SHIT")

      role = discord.utils.get(server.roles, name = 'Grandmaster')
      for member in Grandmaster:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Master')  
      for member in Master:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'Expert')
      for member in Expert:
        if member in Unassigned:
          Unassigned.remove(member)
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role)
      role = discord.utils.get(server.roles, name = 'unassigned')
      for member in Unassigned:
        await client.remove_roles(member, *member.roles)
        await client.add_roles(member, role) 

keep_alive()
BOT_TOKEN = env_vals.get_bot_token()
client.run(BOT_TOKEN)
