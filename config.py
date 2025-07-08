import os

import dotenv

dotenv.load_dotenv()

discordToken = os.environ["DISCORD_TOKEN"]
hypixelKey = os.environ["HYPIXEL_TOKEN"]

helpPlayerCommands = """
`$profile [player name]` - Displays general stats such as network level.
`$uuid [player name]` - Displays UUID of a player.
"""

helpGuildCommands = """
`$guild [guild name]` - Displays stats about a guild.
`$guild player [player name]` - Displays stats about the guild a player is in.
"""

helpBedwarsCommands = """
`$bedwars [player name] [mode]` - Displays a player's stats in Bedwars.
`$bedwars [player name] misc [mode]` - Displays miscellaneous stats about a player.
`$bedwars [player name] kills [mode]` - Displays stats about your kills and deaths.
"""

errorTemplate = """An error has occured:
```
{error}
```
"""

bedWarsInvalidMode = """Invalid gamemode. List of valid gamemodes:
```
{modes}
```
"""

bedwarsResourcesCollected = """Total - `{total}`
Iron - `{iron}`
Gold - `{gold}`
Diamonds - `{diamonds}`
Emeralds - `{emeralds}`
"""

bedwarsItemsPurchased = """Total - `{total}`
Permanent - `{permanent}`
"""

footerText = "Bot made by @vk6"