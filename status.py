import requests, replit

hypixel_key = replit.db["key-hypixel"]

def getStatus(profile):
  uuid = profile["id"]
  r = requests.get("https://api.hypixel.net/status?key={key}&uuid={uuid}".format(key=hypixel_key,uuid=uuid))
  status = r.json()["session"]
  return status
