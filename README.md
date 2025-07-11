## Hypixel Discord Bot
This is a Discord bot that fetches stats for the Hypixel Minecraft server.

### Deployment:

Create a Python venv and install dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Create a .env file with the following contents:

```
DISCORD_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HYPIXEL_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Run the bot:
```
python3 bot.py
```

### Current Commands:


`$profile [player name]` - Displays general stats such as network level. 

`$uuid [player name]` - Displays UUID of a player.

`$guild [guild name]` - Displays stats about a guild.

`$guild player [player name]` - Displays stats about the guild a player is in.

`$bedwars [player name] (mode)` - Displays a player's stats in Bedwars.

`$bedwars [player name] misc (mode)` - Displays miscellaneous stats about a player.

`$bedwars [player name] kills (mode)` - Displays stats about your kills and deaths.

### Todo:
- Add commands for other minigames
- Show quick buy menu and hotbar in bedwars

### License:

```
ading2210/hypixel-discord-bot: a discord bot for hypixel stats
Copyright (C) 2025 ading2210

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```