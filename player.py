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

def getHypixelProfile(profile):
  uuid = profile["id"]
  r = requests.get("https://api.hypixel.net/player?key={key}&uuid={uuid}".format(key=hypixel_key, uuid=uuid))
  hypixelProfile = r.json()["player"]
  return hypixelProfile
  #warning: returns a LOT of data

def getRank(hypixelProfile):
  rankLocations = ["packageRank", "newPackageRank", "monthlyPackageRank", "rank"]
  isStaff = False
  rank = ""
  for location in rankLocations:
    if location in hypixelProfile:
      rank = hypixelProfile[location]

  rank = rank.upper().replace("PLUS","+")
  rank = rank.replace("_", "")
  rank = rank.replace("SUPERSTAR", "MVP++")
  rank = rank.replace("YOUTUBER","YOUTUBE")
  if rank == "":
    return "NONE"
  return rank

def getLevel(hypixelProfile):
  if not "networkExp" in hypixelProfile:
    return 0
  exp = hypixelProfile["networkExp"]

  base = 10000
  growth = 2500

  reverse_pq_prefix = -(base - 0.5 * growth)/growth
  reverse_const = reverse_pq_prefix * reverse_pq_prefix
  growth_divides_2 = 2/growth

  level = math.floor(1+reverse_pq_prefix + math.sqrt(reverse_const+growth_divides_2*exp))

  return level

def formattedTime(unixTimestamp):
  timeObject = datetime.utcfromtimestamp(unixTimestamp)
  formattedTime = timeObject.strftime("%m/%d/%Y, %H:%M:%S (UTC)")
  return formattedTime

def getFirstJoin(hypixelProfile):
  try:
    return formattedTime(int(hypixelProfile["firstLogin"])/1000)
  except:
    return "Unknown"

def getLatestJoin(hypixelProfile):
  try:
    return formattedTime(int(hypixelProfile["lastLogin"])/1000)
  except:
    return "Unknown"