import player

gamemodeDict = {
  "solos": "eight_one",
  "doubles": "eight_two",
  "threes": "four_three",
  "fours": "four_four",
  "rush_fours": "four_four_rush",
  "rush_doubles": "eight_two_rush",
  "lucky_fours": "four_four_lucky",
  "lucky_doubles": "eight_two_lucky",
  "underworld_fours": "four_four_underworld",
  "underworld_doubles": "eight_two_underworld",
  "armed_fours": "four_four_armed",
  "armed_doubles": "eight_two_armed",
  "ultimate": "four_four_ultimate",
  "voidless": "four_four_voidless",
  "castle": "castle",
  "4v4": "two_four",
  "swap_fours": "four_four_swap",
  "swap_doubles": "eight_two_swap"
}
deathMethods = [
  "entity_attack",
  "void",
  "fall",
  "projectile",
  "magic",
  "entity_explosion",
  "fire_tick",
  "suffocation"
]
finalDeathMethods = [
  "entity_attack",
  "void",
  "fall",
  "projectile",
  "magic",
  "entity_explosion",
  "fire_tick"
]
killMethods = [
  "entity_attack",
  "void",
  "fall",
  "projectile",
  "magic",
  "entity_explosion",
  "fire_tick"
]
finalKillMethods = killMethods

def convertGamemode(gamemode):
  if gamemode in gamemodeDict:
    return gamemodeDict[gamemode]
  return ""

class BedwarsStats():
  def __init__(self, profileDict=None, name=None):
    if not profileDict == None:
      self.profileDict = profileDict
    elif not name == None:
      profile = player.getProfile(name)
      self.profileDict = player.getprofileDict(profile)
    else:
      raise Exception("No arguments provided.")
    if self.profileDict == None:
      raise KeyError("User has no stats.")
    if not "Bedwars" in self.profileDict["stats"]:
      raise KeyError("User has no stats.")
    self.statsDict = self.profileDict["stats"]["Bedwars"]

  def coins(self):
    key = "coins"
    if key in self.statsDict:
      return self.statsDict[key]
    return 0

  def deaths(self, mode="", cause=""):
    key = "_".join([mode, cause, "deaths_bedwars"])
    key = key.replace("__","_")
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def kills(self, mode="", cause=""):
    key = "_".join([mode, cause, "kills_bedwars"])
    key = key.replace("__","_")
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0

  def kdr(self, mode=""):
    deaths = self.deaths(mode=mode)
    if deaths == 0:
      return float('Inf')
    return round(self.kills(mode=mode)/deaths, 2)

  def finalDeaths(self, mode="", cause=""):
    key = "_".join([mode, cause, "final_deaths_bedwars"])
    key = key.replace("__","_")
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def finalKills(self, mode="", cause=""):
    key = "_".join([mode, cause, "final_kills_bedwars"])
    key = key.replace("__","_")
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def fkdr(self, mode=""):
    finals = self.finalDeaths(mode=mode)
    if finals == 0:
      return float('Inf')
    return round(self.finalKills(mode=mode)/finals, 2)

  def wins(self, mode=""):
    key = "_".join([mode, "wins_bedwars"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def losses(self, mode=""):
    key = "_".join([mode, "losses_bedwars"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def wlr(self, mode=""):
    losses = self.losses(mode=mode)
    if losses == 0:
      return float('Inf')
    return round(self.wins(mode=mode)/losses, 2)

  def bedBreaks(self, mode=""):
    key = "_".join([mode, "beds_broken_bedwars"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def bedsLost(self, mode=""):
    key = "_".join([mode, "beds_lost_bedwars"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def bblr(self, mode=""):
    bedsLost = self.bedsLost(mode=mode)
    if bedsLost == 0:
      return float('Inf')
    return round(self.bedBreaks(mode=mode)/bedsLost, 2)
  
  def level(self):
    if "bedwars_level" in self.profileDict["achievements"]:
      return self.profileDict["achievements"]["bedwars_level"]
    return 0

  def winstreak(self,  mode=""):
    key = "_".join([mode, "winstreak"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0

  def resourcesCollected(self, mode="", resourceType=""):
    key = "_".join([mode, resourceType, "resources_collected_bedwars"])
    key = key.replace("__","_")
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0

  def itemsPurchased(self, mode=""):
    key = "_".join([mode, "_items_purchased_bedwars"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key == "_items_purchased_bedwars":
      key = "items_purchased_bedwars"
    if key in self.statsDict:
      return self.statsDict[key]
    return 0
  
  def itemsPurchasedPermanent(self, mode=""):
    modeString = "_".join([mode, "permanent"])
    if modeString.startswith("_"):
      modeString = modeString.replace("_","",1)
    if modeString.endswith("_"):
      modeString = modeString[:-1]
    key = " ".join([modeString, "_items_purchased_bedwars"])
    keyAlt = key.replace(" ", "")
    if key in self.statsDict and keyAlt in self.statsDict:
      if self.statsDict[key] > self.statsDict[keyAlt]:
        return self.statsDict[key]
      return self.statsDict[keyAlt]
    if key in self.statsDict:
      return self.statsDict[key]
    if key.replace(" ", "") in self.statsDict:
      return self.statsDict[key.replace(" ", "")]
    return 0
  
  def gamesPlayed(self, mode=""):
    key = "_".join([mode, "games_played_bedwars"])
    if key.startswith("_"):
      key = key.replace("_","",1)
    if key in self.statsDict:
      return self.statsDict[key]
    return 0