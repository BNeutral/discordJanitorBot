# Purpose

This bot will force a one message per user limit on a channel (retroactively), and cleans letter reactions from one channel (not retroactively). Messages deleted from the channel will be logged to another channel.

# Requirements

* Python 3
* Create an application on Discord's developer portal: https://discordapp.com/developers/applications/
* Install pip (python packet manager) and run `pip install -U discord.py`

# Setup

* Add the bot to your server using the link created at the discord dev page for the app, under OAuth2 submenu, by clicking the bot checkbox
* Create a secrets.py file with the content:

```
BOT_TOKEN = <your bot token here, as a string. For example "Aao23...">
```

# Run

python ./janibot.py