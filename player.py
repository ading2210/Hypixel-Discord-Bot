import requests, math, replit
from datetime import datetime

hypixel_key = replit.db["key-hypixel"]

def getProfile(name):
  r = requests.get("https://api.mojang.com/users/profiles/minecraft/{name}".format(name=name))
  try:
    profile = r.json()
  except:
    return {"error":"Invalid name"}
  return profile

def getProfileUuid(uuid):
  r = requests.get("https://api.mojang.com/user/profiles/{uuid}/names".format(uuid=uuid))
  try:
    profile = {"name":r.json()[-1].get('name'),"id":uuid}
  except:
    return {"error":"Invalid uuid"}
  return profile

def getprofileDict(profile):
  uuid = profile["id"]
  r = requests.get("https://api.hypixel.net/player?key={key}&uuid={uuid}".format(key=hypixel_key, uuid=uuid))
  profileDict = r.json()["player"]
  return profileDict
  #warning: returns a LOT of data

def formattedTime(unixTimestamp):
  timeObject = datetime.utcfromtimestamp(unixTimestamp)
  formattedTime = timeObject.strftime("%m/%d/%Y, %H:%M:%S (UTC)")
  return formattedTime

class HypixelProfile():
  def __init__(self, profile=None):
    self.profileDict = getprofileDict(profile)

  def rank(self):
    rankLocations = ["packageRank", "newPackageRank", "monthlyPackageRank", "rank"]
    isStaff = False
    rank = ""
    for location in rankLocations:
      if location in self.profileDict:
        rank = self.profileDict[location]

    rank = rank.upper().replace("PLUS","+")
    rank = rank.replace("_", "")
    rank = rank.replace("SUPERSTAR", "MVP++")
    rank = rank.replace("YOUTUBER","YOUTUBE")
    if rank == "":
      return "NONE"
    return rank

  def latestGame(self):
    if "mostRecentGameType" in self.profileDict:
      return self.profileDict["mostRecentGameType"]
    else: 
      return "Unknown"

  def rankFormatted(self):
    rank = self.rank()
    if rank == "NONE":
      return ""
    else:
      return "[{rank}] ".format(rank=rank)

  def level(self):
    if not "networkExp" in self.profileDict:
      return 0
    exp = self.profileDict["networkExp"]

    base = 10000
    growth = 2500

    reverse_pq_prefix = -(base - 0.5 * growth)/growth
    reverse_const = reverse_pq_prefix * reverse_pq_prefix
    growth_divides_2 = 2/growth

    level = math.floor(1+reverse_pq_prefix + math.sqrt(reverse_const+growth_divides_2*exp))

    return level

  def firstJoin(self):
    try:
      return formattedTime(int(self.profileDict["firstLogin"])/1000)
    except:
      return "Unknown"

  def latestJoin(self):
    try:
      return formattedTime(int(self.profileDict["lastLogin"])/1000)
    except:
      return "Unknown"