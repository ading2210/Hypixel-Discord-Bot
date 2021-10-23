from replit import db
import discord, requests
from discord.ext import commands
import player, status, guild, messages

token = db["token"]
hypixel_key = db["key-hypixel"]

bot = commands.Bot(command_prefix="$", help_command=None)

@bot.event
async def on_ready():
  print(f'Bot connected as {bot.user}')

@bot.command(name="help")
async def helpCommand(ctx):
  embed=discord.Embed(title="Command List:", color=0xffaa00)
  embed.set_thumbnail(url="https://cdn.discordapp.com/icons/489529070913060867/f7df056de15eabfc0a0e178d641f812b.webp")
  embed.add_field(name="Player Commands:", value=messages.helpPlayerCommands, inline=False)
  embed.add_field(name="Guild Commands:", value=messages.helpGuildCommands, inline=False)
  embed.set_footer(text="Bot made vk6#7391")

  await ctx.send(embed=embed)

@bot.command(name="uuid")
async def getUuid(ctx, arg=None):
  if arg == None:
    await ctx.send("Username required.")
    return
  profile = player.getProfile(arg)
  await ctx.send("**UUID of user {user}:**\n```{uuid}```".format(uuid=profile["id"], user=profile["name"]))

@bot.command(name="profile")
async def getProfile(ctx, name=None):
  if name == None:
    await ctx.send("Username required.")
    return
  profile = player.getProfile(name)
  if "error" in profile:
    await ctx.send("Invalid username or arguments.")
    return
  
  hypixelProfile = player.HypixelProfile(profile)
  name = profile["name"]
  uuid = profile["id"]
  rank = hypixelProfile.rank()
  statusData = status.getStatus(profile)

  if statusData["online"] == True:
    currentGame = statusData["gameType"] + " - " + statusData["mode"]
  
  rankFormatted = hypixelProfile.rankFormatted()
  lastGame = hypixelProfile.latestGame()
  level = hypixelProfile.level()
  firstJoin = hypixelProfile.firstJoin()
  latestJoin = hypixelProfile.latestJoin()

  playerGuild = guild.getGuildDictByPlayer(profile)
  if playerGuild == None:
    guildName = "None"
  else:
    guildName = playerGuild["name"]

  embed=discord.Embed(title="Player info for {rank}{player}:".format(player=name, rank=rankFormatted), color=0xffaa00)
  embed.set_thumbnail(url="https://mc-heads.net/body/{uuid}/left/100.png".format(uuid=uuid))
  embed.add_field(name="Rank:", value="`"+rank+"`", inline=False)
  embed.add_field(name="Network Level:", value="`"+str(level)+"`", inline=False)
  embed.add_field(name="Guild:", value="`"+guildName+"`", inline=False)
  embed.add_field(name="Online?", value="`"+str(statusData["online"])+"`", inline=False)
  embed.add_field(name="First Join:", value="`"+firstJoin+"`", inline=False)
  if statusData["online"] == False:
    embed.add_field(name="Last Online:", value="`"+latestJoin+"`", inline=False)
    embed.add_field(name="Last Game:", value="`"+lastGame+"`", inline=False)
  else:
    embed.add_field(name="Currently Playing:", value="`"+currentGame+"`", inline=False)
  embed.set_footer(text="Bot made by vk6#7391")
  
  await ctx.send(embed=embed)

@bot.command(name="guild")
async def getGuild(ctx, arg1=None, arg2=None):
  name = arg1
  if arg2 == None:
    if name == None:
      await ctx.send("Guild name required.")
      return
    playerGuild = guild.Guild(name=name)
  else:
    playerName = arg2
    playerProfile = player.getProfile(playerName)
    playerGuild = guild.Guild(player=playerProfile)
  guildDict = playerGuild.guildDict
  if guildDict == None:
    await ctx.send("Invalid guild or player name, or user is not part of any guild.")
    return
  guildName = playerGuild.name()
  tag = playerGuild.tag()
  description = playerGuild.description()
  createdDate = playerGuild.createdDateFormatted()
  memberCount = playerGuild.memberCount()
  level = playerGuild.level()

  embed=discord.Embed(title="Guild info for guild {guildName}:".format(guildName=guildName), color=0xffaa00)
  embed.set_thumbnail(url="https://cdn.discordapp.com/icons/489529070913060867/f7df056de15eabfc0a0e178d641f812b.webp")
  embed.add_field(name="Tag:", value="`"+tag+"`", inline=False)
  embed.add_field(name="Description:", value="`"+description+"`", inline=False)
  embed.add_field(name="Level:", value="`"+str(level)+"`", inline=False)
  embed.add_field(name="Member Count:", value="`"+str(memberCount)+"/125"+"`", inline=False)
  embed.add_field(name="Date Created:", value="`"+createdDate+"`", inline=False)
  embed.set_footer(text="Bot made vk6#7391")
  await ctx.send(embed=embed)
  
bot.run(token)