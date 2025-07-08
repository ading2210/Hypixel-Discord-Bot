import requests
import config

def getStatus(profile):
  uuid = profile["id"]
  r = requests.get("https://api.hypixel.net/status?key={key}&uuid={uuid}".format(key=config.hypixelKey, uuid=uuid))
  status = r.json()["session"]
  return status
