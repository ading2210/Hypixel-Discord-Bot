import math

import requests

import player
import config

def getGuildDictByPlayer(profile):
  uuid = profile["id"]
  r = requests.get("https://api.hypixel.net/guild?key={key}&player={uuid}".format(key=config.hypixelKey,uuid=uuid))
  guildDict = r.json()["guild"]
  return guildDict

def getGuildDictByName(name):
  r = requests.get("https://api.hypixel.net/guild?key={key}&name={name}".format(key=config.hypixelKey,name=name))  
  guildDict = r.json()["guild"]
  return guildDict

class Guild():
  def __init__(self, player=None, name=None, guildDict=None):
    if not player == None:
      guildDict = getGuildDictByPlayer(player)
    elif not name == None:
      guildDict = getGuildDictByName(name)
    else:
      raise Exception("No arguments provided.")

    self.guildDict = guildDict

  def name(self):
    name = self.guildDict["name"]
    return name
    
  def owner(self):
    uuid = self.guildDict["members"][0]["uuid"]
    owner = player.getProfileUuid(uuid)
    return owner

  def tag(self):
    if "tag" in self.guildDict:
      return self.guildDict["tag"]
    return "None"

  def description(self):
    if "description" in self.guildDict:
      return self.guildDict["description"]
    return "None"

  def createdDateFormatted(self):
    if "created" in self.guildDict:
      timeFormatted = player.formattedTime(int(self.guildDict["created"])/1000)
      return timeFormatted
    return "Unknown"

  def memberCount(self):
    if "members" in self.guildDict:
      return len(self.guildDict["members"])
    return 0

  def exp(self):
    if "exp" in self.guildDict:
      return self.guildDict["exp"]
    return 0
  
  def level(self):
    #Why does hypixel have to hard code these values?
    #Based on https://hypixel.net/threads/hypixel-guild-xp-to-level-php.1774806/post-13656451
    #Translated into Python from PHP

    exp = self.exp()

    if exp < 100000:
      return 0
    elif exp < 250000:
      return 1
    elif exp < 500000:
      return 2
    elif exp < 1000000:
      return 3
    elif exp < 1750000:
      return 4
    elif exp < 2750000:
      return 5
    elif exp < 4000000:
      return 6
    elif exp < 5500000:
      return 7
    elif exp < 7500000:
      return 8
    else:
      if exp < 15000000:
        return math.floor((exp - 7500000) / 2500000) + 9
      else:
        return math.floor((exp - 15000000) / 3000000) + 12