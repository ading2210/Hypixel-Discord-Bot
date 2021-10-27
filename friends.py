import player, config, requests, math

class FriendItem():
  def __init__(self, friendItemDict=None, playerUuid=None):
    if friendItemDict == None or playerUuid == None:
      raise Exception("No player provided.")
    self.friendItemDict = friendItemDict
    self.playerUuid = playerUuid

  def uuid(self):
    if self.friendItemDict["uuidReceiver"] == self.playerUuid:
      return self.friendItemDict["uuidSender"]
    return self.friendItemDict["uuidReceiver"]

  def hypixelProfile(self):
    if not "hypixelProfile" in self.friendItemDict:
      self.friendItemDict["hypixelProfile"] = player.HypixelProfile(profileDict=player.getprofileDict(uuid=self.uuid()))
    return self.friendItemDict["hypixelProfile"]

  def name(self):
    if not "hypixelProfile" in self.friendItemDict:
      self.hypixelProfile()
    return self.hypixelProfile().name()

  def rank(self):
    if not "hypixelProfile" in self.friendItemDict:
      self.hypixelProfile()
    return self.hypixelProfile().rank()

  def rankFormatted(self):
    if not "hypixelProfile" in self.friendItemDict:
      self.hypixelProfile()
    return self.hypixelProfile().rankFormatted()

  def dateAdded(self):
    return self.friendItemDict["started"]

  def dateAddedFormatted(self):
    return player.formattedTime(self.dateAdded()/1000)

class PlayerFriends():
  def __init__(self, profile=None):
    if profile == None:
      raise Exception("No player provided.")
    self.uuid = profile["id"]
    r = requests.get("https://api.hypixel.net/friends?key={key}&uuid={uuid}".format(key=config.hypixelKey, uuid=self.uuid))
    self.friendsListRaw = r.json()["records"]
    self.friendsList = []
    for friend in self.friendsListRaw:
      self.friendsList.append(FriendItem(friendItemDict=friend, playerUuid=self.uuid))

  def count(self):
    return len(self.friendsList)

  def all(self):
    return self.friendsList

  def page(self, page=1, size=20):
    if len(self.friendsList) < size:
      return self.friendsList
    return self.friendsList[(page-1)*size:page*size]

  def pages(self, size=20):
    pageCount = math.floor(len(self.friendsList)/size)+1
    return pageCount