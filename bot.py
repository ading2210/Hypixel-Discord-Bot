from replit import db
import discord, requests, json
from discord.ext import commands
import player, status, guild, messages, bedwars

configFile = open("config.json")
config = json.load(configFile)
configFile.close()

token = db["token"]
hypixel_key = db["key-hypixel"]

activity = discord.Activity(type=discord.ActivityType.watching, name="$help")
bot = commands.Bot(command_prefix="$", help_command=None, activity=activity)

@bot.event
async def on_ready():
  print(f'Bot connected as {bot.user}')

@bot.command(name="help")
async def helpCommand(ctx):
  embed=discord.Embed(title="Command List:", color=0xffaa00)
  embed.set_thumbnail(url="https://cdn.discordapp.com/icons/489529070913060867/f7df056de15eabfc0a0e178d641f812b.webp")
  embed.add_field(name="Player Commands:", value=messages.helpPlayerCommands, inline=False)
  embed.add_field(name="Guild Commands:", value=messages.helpGuildCommands, inline=False)
  embed.add_field(name="Bedwars Commands:", value=messages.helpBedwarsCommands, inline=False) 
  embed.set_footer(text="Bot made by vk6#7391")

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

  embed=discord.Embed(title="Player info for `{rank}{player}`:".format(player=name, rank=rankFormatted), color=0xffaa00)
  embed.set_thumbnail(url="https://mc-heads.net/body/{uuid}/left/100.png".format(uuid=uuid))
  embed.add_field(name="Rank:", value="`"+rank+"`", inline=True)
  embed.add_field(name="Network Level:", value="`"+str(level)+"`", inline=True)
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

  embed=discord.Embed(title="Guild info for guild `{guildName}`:".format(guildName=guildName), color=0xffaa00)
  embed.set_thumbnail(url="https://cdn.discordapp.com/icons/489529070913060867/f7df056de15eabfc0a0e178d641f812b.webp")
  embed.add_field(name="Tag:", value="`"+tag+"`", inline=True)
  embed.add_field(name="Level:", value="`"+str(level)+"`", inline=True)
  embed.add_field(name="Member Count:", value="`"+str(memberCount)+"/125"+"`", inline=True)
  embed.add_field(name="Description:", value="`"+description+"`", inline=False)
  embed.add_field(name="Date Created:", value="`"+createdDate+"`", inline=False)
  embed.set_footer(text="Bot made by vk6#7391")
  await ctx.send(embed=embed)

@bot.command(name="bedwars", aliases=["bw"])
async def bedstats(ctx, arg1=None, arg2=None, arg3=None):
  async def returnModes(ctx):
    modeList = []
    for mode in bedwars.gamemodeDict.keys():
      modeList.append("- {mode}".format(mode=mode))
    modeListString = "\n".join(modeList)
    await ctx.send(messages.bedWarsInvalidMode.format(modes=modeListString))

  modeFormatted = ""
  if arg1 == None:
    await ctx.send("Username required.")
    return
  mode = bedwars.convertGamemode(arg2)
  if arg2 == "misc" or arg2 == "kills":
    if arg3 == None:
      mode = ""
      modeFormatted = "Overall"
    else:
      mode = bedwars.convertGamemode(arg3)
      modeFormatted = arg3.replace("_"," ").title()
  if arg2 == None or ((arg2 == "misc" or arg2 == "kills") and arg3 == None):
    modeFormatted = "Overall"
  elif not arg2 == None and not (arg2 == "misc" or arg2 == "kills"):
    modeFormatted = arg2.replace("_"," ").title()
    if mode == "":
      await returnModes(ctx)
      return

  if arg3 == None and (arg2 == "misc" or arg2 == "kills"):
    modeFormatted = "Overall"
  elif not arg3 == None:
    if not arg3 in bedwars.gamemodeDict.keys():
      await returnModes(ctx)
      return
    modeFormatted = arg3.replace("_"," ").title()
        
  profile = player.getProfile(arg1)
  if not "id" in profile:
    await ctx.send("Invalid username or arguments.")
    return
  hypixelProfile = player.HypixelProfile(profile)
  if "error" in profile:
    await ctx.send("Invalid username or arguments.")
    return
  name = profile["name"]
  uuid = profile["id"]

  try:
    bedstats = bedwars.BedwarsStats(name=name)
  except KeyError as e:
    error = "An error occured:\n```"+str(e).strip("'")+"```"
    await ctx.send(error)
    return

  level = bedstats.level()
  levelFormatted = "[{level}☆] ".format(level=str(level))
  rank = hypixelProfile.rankFormatted()
  fkdr = bedstats.fkdr(mode=mode)
  finalKills = bedstats.finalKills(mode=mode)
  finalDeaths = bedstats.finalDeaths(mode=mode)
  kdr = bedstats.kdr(mode=mode)
  kills = bedstats.kills(mode=mode)
  deaths = bedstats.deaths(mode=mode)
  bblr = bedstats.bblr(mode=mode)
  bedBreaks = bedstats.bedBreaks(mode=mode)
  bedsLost = bedstats.bedsLost(mode=mode)
  wlr = bedstats.wlr(mode=mode)
  wins = bedstats.wins(mode=mode)
  losses = bedstats.losses(mode=mode)
  winstreak = bedstats.winstreak(mode=mode)

  iconURL = config["webUrl"] + "/static/images/bedwars_icon.png"
  avatarURL = "https://mc-heads.net/body/{uuid}/50.png".format(uuid=uuid)
  embed=discord.Embed(title="Bedwars stats for `{level}{rank}{name}`:".format(name=name, rank=rank,level=levelFormatted), color=0xffaa00)
  embed.set_thumbnail(url=iconURL)

  if arg2 == "misc":
    gamesPlayed = bedstats.gamesPlayed(mode=mode)
    resourcesCollected = bedstats.resourcesCollected(mode=mode)
    ironCollected = bedstats.resourcesCollected(mode=mode, resourceType="iron")
    goldCollected = bedstats.resourcesCollected(mode=mode, resourceType="gold")
    diamondsCollected = bedstats.resourcesCollected(mode=mode, resourceType="diamond")
    emeraldsCollected = bedstats.resourcesCollected(mode=mode, resourceType="emerald")
    resourcesCollectedString = messages.bedwarsResourcesCollected.format(total=str(resourcesCollected), iron=str(ironCollected), gold=str(goldCollected), diamonds=str(diamondsCollected), emeralds=str(emeraldsCollected))

    itemsPurchased = bedstats.itemsPurchased(mode=mode)
    itemsPurchasedPermanent = bedstats.itemsPurchasedPermanent(mode=mode)
    itemsPurchacedString = messages.bedwarsItemsPurchased.format(total=itemsPurchased,permanent=itemsPurchasedPermanent)

    embed.add_field(name="Resources Collected:", value=resourcesCollectedString, inline=True)
    embed.add_field(name=chr(173), value=chr(173), inline=True)
    embed.add_field(name="Items Purchased:", value=itemsPurchacedString, inline=True)
    
    embed.add_field(name="Selected Mode:", value="`"+str(modeFormatted)+"`", inline=True)
    embed.add_field(name=chr(173), value=chr(173), inline=True)
    embed.add_field(name="Games Played:", value="`"+str(gamesPlayed)+"`")

  elif arg2 == "kills":
    def getKillMethodString(function, killMethods):
      total = function(mode=mode)
      killMethodsList = ["Total - `{total}`".format(total=str(total))]
      for method in killMethods:
        killsForMethod = function(mode=mode, cause=method)
        killMethodsList.append("{methodFormatted} - `{count}`".format(methodFormatted=method.replace("_", " ").title(),count=str(killsForMethod)))
      killMethodsString = "\n".join(killMethodsList)
      return killMethodsString

    embed.add_field(name="Kills:", value=getKillMethodString(bedstats.kills, bedwars.killMethods), inline=True)
    embed.add_field(name=chr(173), value=chr(173), inline=True)
    embed.add_field(name="Deaths:", value=getKillMethodString(bedstats.deaths, bedwars.deathMethods), inline=True)

    embed.add_field(name="Final Kills:", value=getKillMethodString(bedstats.finalKills,bedwars.finalKillMethods), inline=True)
    embed.add_field(name=chr(173), value=chr(173), inline=True)
    embed.add_field(name="Final Deaths:", value=getKillMethodString(bedstats.finalDeaths, bedwars.finalDeathMethods), inline=True)

    embed.add_field(name="Selected Mode:", value="`"+str(modeFormatted)+"`", inline=True)

  elif not arg2 == "misc":
    embed.add_field(name="FKDR:", value="`"+str(fkdr)+"`", inline=True)
    embed.add_field(name="Final Kills:", value="`"+str(finalKills)+"`", inline=True)
    embed.add_field(name="Final Deaths:", value="`"+str(finalDeaths)+"`", inline=True)
    embed.add_field(name="KDR:", value="`"+str(kdr)+"`", inline=True)
    embed.add_field(name="Kills:", value="`"+str(kills)+"`", inline=True)
    embed.add_field(name="Deaths:", value="`"+str(deaths)+"`", inline=True)
    embed.add_field(name="BBLR:", value="`"+str(bblr)+"`", inline=True)
    embed.add_field(name="Bed Broken:", value="`"+str(bedBreaks)+"`", inline=True)
    embed.add_field(name="Beds Lost:", value="`"+str(bedsLost)+"`", inline=True)
    embed.add_field(name="WLR:", value="`"+str(wlr)+"`", inline=True)
    embed.add_field(name="Wins:", value="`"+str(wins)+"`", inline=True)
    embed.add_field(name="Losses:", value="`"+str(losses)+"`", inline=True)
    embed.add_field(name="Selected Mode:", value="`"+str(modeFormatted)+"`", inline=True)
    embed.add_field(name="Winstreak:", value="`"+str(winstreak)+"`", inline=True)

  embed.set_image(url=avatarURL)
  embed.set_footer(text="Bot made by vk6#7391")

  await ctx.send(embed=embed)
  
bot.run(token) 