# Purpose

This bot will force a one message per user limit on a channel by deleting old messages from unique users (retroactively on startup), and cleans letter reactions from messages in one channel (not retroactively). Messages deleted from the channel will be logged to another channel (for moderation purposes) and also sent to the user (in case of accidental double posting).

# Requirements

* Python 3
* Create an application on Discord's developer portal: https://discordapp.com/developers/applications/
* Install pip (python packet manager) and run `pip install -U discord.py`

# Setup

* Add the bot to your server using the link created at the discord dev page for the app, under OAuth2 submenu, by clicking the bot checkbox. Bot permissions needed are be manage messages, read messages, read message history.
* Modify config.py to your liking
* Create a secrets.py file with the content:

```
BOT_TOKEN = <your bot token here, as a string. For example "Aao23...">
```

# Run

python ./janibot.py
