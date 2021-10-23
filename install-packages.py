import os

try:
  import discord
except ModuleNotFoundError:
  print("Installing packages...")
  os.system("pip3 install py-cord flask --disable-pip-version-check")
