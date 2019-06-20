#pip install -U discord.py
#Python 3
import discord
from config import *
from secrets import *
import logging
from collections import defaultdict

#bot requires manage_messages permission
#Logger
logger = logging.getLogger('discord')
logger.setLevel(LOG_LEVEL)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class MyClient(discord.Client):

    def __init__(self):
        super().__init__(fetch_offline_members=True,activity=discord.Activity(name=ACTIVITY,type=discord.ActivityType.playing))
        self.announcementChannel = None
        self.shopChannel = None
        self.logChannel = None
        self.userPosts = defaultdict(list)
        self.userPostIDs = set()

    #Method for logging things both to text log and to a channel
    async def log(self, message, deletedMessage):
        logger.info(message)
        return await self.logChannel.send(message, embed=self.makeEmbed(deletedMessage))

    #Method for logging things both to console and to a text log
    def logLocal(self, message):
        logger.info(message)
        print(message)

    async def on_connect(self):
        self.logLocal("Connected")

    #Overload. See discord.py's Client documentation
    async def on_ready(self):
        self.logLocal(MSG_FINISHED_LOADING.format(self.user))
        self.userPosts = defaultdict(list)
        self.userPostIDs = set()
        self.announcementChannel = self.get_channel(ANNOUNCEMENT_CH_ID)
        self.shopChannel = self.get_channel(SHOP_CH_ID)
        self.logChannel = self.get_channel(LOG_CH_ID)
        await self.loadMessages()

    #TODO: Clump all the awaits at the end of the loop for better performance
    async def loadMessages(self):
        self.logLocal("Doing startup cleaning")
        #messages = await channel.history(limit=5000).flatten()
        async for elem in self.shopChannel.history(limit=10000):
            await self.checkMessage(elem)
        self.logLocal("Done with startup cleaning")

    #Checks a message against the loaded state of the bot and deletes it if it's older
    async def checkMessage(self, discordMessage):
        try:
            for role in discordMessage.author.roles:
                if role.id in IGNORED_SHOP_ROLES:
                    return
        except:
            pass
        authorID = discordMessage.author.id    
        if discordMessage.id not in self.userPostIDs:
            self.userPosts[authorID].append(discordMessage)
            self.userPosts[authorID].sort(key=lambda x: x.created_at,reverse=True)
            self.userPostIDs.add(discordMessage.id)
        while len(self.userPosts[authorID]) > 1:
            message = self.userPosts[authorID].pop() 
            self.userPostIDs.remove(message.id)
            await self.deleteMessage(message)    

    #Deletes a message, logs, and messages the user
    #TODO: Clump up the awaits for some better performance
    async def deleteMessage(self, message):
        author = message.author
        content = message.content
        try :
            await message.delete()
            await self.log(MSG_DELETE_LOG.format(author.name+"#"+str(author.discriminator)), message)
            await author.send(MSG_DELETED_POST.format(author.display_name,content), embed=self.makeEmbed(message))
        except:
            pass

    #Overload. See discord.py's Client documentation
    async def on_message(self, message):
        if message.channel.id != SHOP_CH_ID:
            return
        await self.checkMessage(message)

    #Overload. See discord.py's Client documentation
    #payload members: message_id, user_id, channel_id, guild_id, emoji
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != ANNOUNCEMENT_CH_ID:
            return
        message = await self.announcementChannel.fetch_message(payload.message_id)
        user = message.guild.get_member(payload.user_id)
        if message == None:
            await self.log(MSG_FETCH_ERROR.format(payload.message_id), message)
            return
        for reaction in message.reactions:
            if reaction.emoji in BANNED_REACTIONS:
                await reaction.remove(user)

    #Makes an embed out of a message and returns it
    def makeEmbed(self, message):
        author = message.author
        embed=discord.Embed(color=0xdd5f53)
        embed.timestamp = message.created_at
        embed.set_author(name=(MSG_EMBED_AUTHOR.format(author.name,author.discriminator,author.id)),icon_url=author.avatar_url._url)
        embed.add_field(name=MSG_EMBED_TITLE, value=message.content, inline=True)
        return embed

if __name__ == '__main__':
    client = MyClient()
    client.run(BOT_TOKEN)

