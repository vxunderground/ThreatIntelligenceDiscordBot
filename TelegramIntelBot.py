import time
from discord import Webhook, RequestsWebhookAdapter
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import JoinChannelRequest

DownloadPath = "/home/pi/Telegram/Images/" ##file save path goes here
TelegramClientObject = TelegramClient("BotName", "API-ID", "API-KEY") ##telegram api stuff goes here
TelegramClientObject.start()

ArvinGroup = TelegramClientObject.get_entity("https://t.me/arvin_club")
VxUnderground = TelegramClientObject.get_entity("https://t.me/vxunderground")
Malpedia = TelegramClientObject.get_entity("https://t.me/malpedia")
LogsFree = TelegramClientObject.get_entity("https://t.me/locativelogsfree")
Darknet = TelegramClientObject.get_entity("https://t.me/dbforall")
GonjeshkeDarand = TelegramClientObject.get_entity("https://t.me/GonjeshkeDarand")
PryntStealer = TelegramClientObject.get_entity("https://t.me/officialpryntsoftware")
SiegedSec = TelegramClientObject.get_entity("https://t.me/SiegedSec")
BreachedForums = TelegramClientObject.get_entity("https://t.me/breached_co")
ArmyofThieves = TelegramClientObject.get_entity("https://t.me/ArmyThieves")
SharpBoys = TelegramClientObject.get_entity("https://t.me/sharpboys_3")
WLxDCONFIGS = TelegramClientObject.get_entity("https://t.me/WLxD_CRX")
TommyFlounder = TelegramClientObject.get_entity("https://t.me/floundertech")
GhostSec = TelegramClientObject.get_entity("https://t.me/GhostSecc")
ConfigMaster = TelegramClientObject.get_entity("https://t.me/config_combos")
Zer0DayLab = TelegramClientObject.get_entity("https://t.me/zer0daylab")
HADESSHOP = TelegramClientObject.get_entity("https://t.me/hadesh0p")
NoHideSpace = TelegramClientObject.get_entity("https://t.me/nohidespace")
KILLNET = TelegramClientObject.get_entity("https://t.me/killnet_reservs")
LOLZTEAM = TelegramClientObject.get_entity("https://t.me/lolz_guru")
Ares = TelegramClientObject.get_entity("https://t.me/aresmainchannel")
ZeroDayToday = TelegramClientObject.get_entity("https://t.me/LearnExploit")
CPartisan = TelegramClientObject.get_entity("https://t.me/cpartisans")
club1337 = TelegramClientObject.get_entity("https://t.me/club1337")
Documentor = TelegramClientObject.get_entity("https://t.me/documentors")
DDoSecrets = TelegramClientObject.get_entity("https://t.me/AntiPlumbers")
SnatchTeam = TelegramClientObject.get_entity("https://t.me/snatch_news")
inj3ct0r = TelegramClientObject.get_entity("https://t.me/inj3ct0rs")
RalfHacker = TelegramClientObject.get_entity("https://t.me/RalfHackerChannel")
RuHeight = TelegramClientObject.get_entity("https://t.me/ruheight")
Data1eaks = TelegramClientObject.get_entity("https://t.me/data1eaks")
R0Crew = TelegramClientObject.get_entity("https://t.me/R0_Crew")
HeawsNet = TelegramClientObject.get_entity("https://t.me/heawsnet")

TelegramClientObject(JoinChannelRequest(VxUnderground))
TelegramClientObject(JoinChannelRequest(ArvinGroup))
TelegramClientObject(JoinChannelRequest(Malpedia))
TelegramClientObject(JoinChannelRequest(LogsFree))
TelegramClientObject(JoinChannelRequest(Darknet))
TelegramClientObject(JoinChannelRequest(GonjeshkeDarand))
TelegramClientObject(JoinChannelRequest(PryntStealer))
TelegramClientObject(JoinChannelRequest(SiegedSec))
TelegramClientObject(JoinChannelRequest(BreachedForums))
TelegramClientObject(JoinChannelRequest(ArmyofThieves))
TelegramClientObject(JoinChannelRequest(SharpBoys))
TelegramClientObject(JoinChannelRequest(WLxDCONFIGS))
TelegramClientObject(JoinChannelRequest(TommyFlounder))
TelegramClientObject(JoinChannelRequest(GhostSec))
TelegramClientObject(JoinChannelRequest(ConfigMaster))
TelegramClientObject(JoinChannelRequest(Zer0DayLab))
TelegramClientObject(JoinChannelRequest(HADESSHOP))
TelegramClientObject(JoinChannelRequest(NoHideSpace))
TelegramClientObject(JoinChannelRequest(KILLNET))
TelegramClientObject(JoinChannelRequest(LOLZTEAM))
TelegramClientObject(JoinChannelRequest(Ares))
TelegramClientObject(JoinChannelRequest(ZeroDayToday))
TelegramClientObject(JoinChannelRequest(CPartisan))
TelegramClientObject(JoinChannelRequest(club1337))
TelegramClientObject(JoinChannelRequest(Documentor))
TelegramClientObject(JoinChannelRequest(DDoSecrets))
TelegramClientObject(JoinChannelRequest(SnatchTeam))
TelegramClientObject(JoinChannelRequest(inj3ct0r))
TelegramClientObject(JoinChannelRequest(RalfHacker))
TelegramClientObject(JoinChannelRequest(RuHeight))
TelegramClientObject(JoinChannelRequest(Data1eaks))
TelegramClientObject(JoinChannelRequest(R0Crew))
TelegramClientObject(JoinChannelRequest(HeawsNet))


TelegramFeed = Webhook.from_url("https://discord.com/api/webhooks/000/0000", adapter=RequestsWebhookAdapter()) ## discord url hook goes here
DiscordClient = discord.Client()

##****Arvin Group handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=ArvinGroup))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("Arvin Group", EventObject.message.message)

##****vx-underground handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=VxUnderground))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("vx-underground", EventObject.message.message)

##****Malpedia handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=Malpedia))
async def EventHandler(EventObject):
    CreateTelegramMessageOutput("Malpedia", EventObject.message.message)

##****LogsFree handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=LogsFree))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("LogsFree", EventObject.message.message)
    
##****Darknet handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=Darknet))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("Darknet", EventObject.message.message)
    
##****GonjeshkeDarand handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=GonjeshkeDarand))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("GonjeshkeDarand", EventObject.message.message)
    
##****PryntStealer handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=PryntStealer))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("PryntStealer", EventObject.message.message)
    
##****SiegedSec handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=SiegedSec))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("SiegedSec", EventObject.message.message)

##****BreachedForums handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=BreachedForums))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("BreachedForums", EventObject.message.message)
    
##****ArmyofThieves handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=ArmyofThieves))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("ArmyofThieves", EventObject.message.message)

##****SharpBoys handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=SharpBoys))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("SharpBoys", EventObject.message.message)

##****WLxDCONFIGS handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=WLxDCONFIGS))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("WLxDCONFIGS", EventObject.message.message)
    
##****TommyFlounder handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=TommyFlounder))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("TommyFlounder", EventObject.message.message)

##****GhostSec handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=GhostSec))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("GhostSec", EventObject.message.message)
    
##****ConfigMaster handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=ConfigMaster))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("ConfigMaster", EventObject.message.message)

##****Zer0DayLab handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=Zer0DayLab))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("Zer0DayLab", EventObject.message.message)

##****HADESSHOP handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=HADESSHOP))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("HADESSHOP", EventObject.message.message)

##****NoHideSpace handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=NoHideSpace))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("NoHideSpace", EventObject.message.message)

##****KILLNET handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=KILLNET))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("KILLNET", EventObject.message.message)

##****LOLZTEAM handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=LOLZTEAM))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("LOLZTEAM", EventObject.message.message)

##****Ares handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=Ares))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("Ares", EventObject.message.message)

##****ZeroDayToday handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=ZeroDayToday))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("ZeroDayToday", EventObject.message.message)
    
##****CPartisan handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=CPartisan))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("CPartisan", EventObject.message.message)
    
##****club1337 handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=club1337))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("club1337", EventObject.message.message)
    
##****Documentor handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=Documentor))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("Documentor", EventObject.message.message)
    
##****DDoSecrets handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=DDoSecrets))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("DDoSecrets", EventObject.message.message)
    
##****SnatchTeam handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=SnatchTeam))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("SnatchTeam", EventObject.message.message)
    
##****inj3ct0r handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=inj3ct0r))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("inj3ct0r", EventObject.message.message)

##****RalfHacker handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=RalfHacker))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("RalfHacker", EventObject.message.message)

##****RuHeight handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=RuHeight))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("RuHeight", EventObject.message.message)

##****Data1eaks handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=Data1eaks))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("Data1eaks", EventObject.message.message)

##****R0Crew handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=R0Crew))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("R0Crew", EventObject.message.message)
    
##****HeawsNet handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=HeawsNet))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("HeawsNet", EventObject.message.message)

##****Telegram string builder****
def CreateTelegramMessageOutput(GroupString, MessageBuffer):
    OutputString = GroupString + " " + time.ctime() + " "
    OutputString += MessageBuffer
    TelegramFeed.send(OutputString)
    
def EntryMain():
    TelegramClientObject.run_until_disconnected()
    
EntryMain()
