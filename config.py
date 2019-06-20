import logging

#LOG
LOG_LEVEL = logging.INFO
LOG_FILE = "janibot.log"

#Channels
ANNOUNCEMENT_CH_ID = 587587541138538506 #testing channel
SHOP_CH_ID = 587587612466872339 #testing channel
LOG_CH_ID = 573404505215991828 #testing channel
#ANNOUNCEMENT_CH_ID = 208152228085760001
#SHOP_CH_ID = 554516380968288296
#LOG_CH_ID = 588909971404750848

#Message exclusions
IGNORED_SHOP_ROLES = set([208152530448809984, 478571196896772098, 208150014638161928, 208151805941645315])
#IGNORED_SHOP_ROLES.add(573412970449600542) #testing

#Emojis
def addLetterEmojis(set) :
    number = 0x1F1E6
    for x in range(26):
        set.add(chr(number+x))

BANNED_REACTIONS = set([u'\U0001F170',u'\U0001F171',u'\U0001F17E',u'\U0001F18E', u'\U0001F595', u'\U0001F194', u'\U0001F191',u'\U0001F196',u'\U0001F197',u'\U0001F198',u'\U0001F19A',u'\U000024C2',u'\U000000A9',u'\U000000AE'])
addLetterEmojis(BANNED_REACTIONS)
ACTIVITY = "Seagull Simulator"
print(BANNED_REACTIONS)

#Message for post deletion
MSG_DELETED_POST = "Hello {0}. Only one post is allowed per person in <#"+str(SHOP_CH_ID)+">. One of your older messages has been deleted.\n"
MSG_FINISHED_LOADING = "Logged on as {0}!" #Console message shown when the bot is ready to work
MSG_FETCH_ERROR = "Error fetching message with id {0}" #Console message shown when there's a failure fetching a message
MSG_DELETE_LOG = "Deleted duplicate message in shops channel by {0}" #Message posted on the discord channel log above the embed
MSG_EMBED_TITLE = "Message deleted" #Embed title
MSG_EMBED_AUTHOR = "{0}#{1} Id:{2}" #Embed author format
