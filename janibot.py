#pip install -U discord.py
#Python 3
import discord
from config import *
from secrets import *
import logging
import asyncio
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
        self.userPosts = defaultdict(list)
        self.announcementChannel = None
        self.shopChannel = None
        self.logChannel = None
        self.fullyReady = asyncio.Event()
        self.lock = asyncio.Lock()

    #Method for logging things both to console and to a channel
    async def log(self, message, deletedMessage):
        logger.info(message)
        return await self.logChannel.send(message, embed=self.makeEmbed(deletedMessage))

    #Overload. See discord.py's Client documentation
    async def on_ready(self):
        print(MSG_FINISHED_LOADING.format(self.user))
        self.announcementChannel = self.get_channel(ANNOUNCEMENT_CH_ID)
        self.shopChannel = self.get_channel(SHOP_CH_ID)
        self.logChannel = self.get_channel(LOG_CH_ID)
        await self.loadMessages()
        self.fullyReady.set()

    #TODO: More async looping
    async def loadMessages(self):
        print("Doing startup cleaning")
        #messages = await channel.history(limit=5000).flatten()
        async for elem in self.shopChannel.history(limit=1000000):
            await self.checkMessage(elem)
        print("Done with startup cleaning")

    #Checks a message against the loaded state of the bot and deletes it if it's older
    async def checkMessage(self, discordMessage):
        try:
            for role in discordMessage.author.roles:
                if role.id in IGNORED_SHOP_ROLES:
                    return
        except:
            pass
        authorID = discordMessage.author.id    
        async with self.lock: #TODO: One lock per user id instead of this if performace is bad
            self.userPosts[authorID].append(discordMessage)
            self.userPosts[authorID].sort(key=lambda x: x.created_at,reverse=True)
            while len(self.userPosts[authorID]) > 1:
                #This is why the lock is needed
                await self.deleteMessage(self.userPosts[authorID].pop())    
        #if authorID in self.userPosts:
        #    if self.userPosts[authorID].created_at >= discordMessage.created_at:
        #        await self.deleteMessage(discordMessage)
        #    else:
        #        message = self.userPosts[authorID]
        #        self.userPosts[authorID] = discordMessage
        #        await self.deleteMessage(message)                
        #else:
        #    self.userPosts[authorID] = discordMessage

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
        await self.fullyReady.wait()
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

