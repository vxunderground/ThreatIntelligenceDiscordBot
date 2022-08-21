import os
import time
from discord import Webhook, RequestsWebhookAdapterv, File
from telethon import TelegramClient, events, sync
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest

# downloads to the TelegramImages directory by default, replace if desired otherwise
image_download_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'TelegramImages')

# put your telegram api stuff in here
telegram_client = TelegramClient('Bot Name', 'API ID', 'API HASH')
telegram_client.start()

# put the discord hook url to the channel you want to receive feeds in here
telegram_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
#discord_client = discord.Client()

telegram_feed_list = {
    'ArvinGroup': 'https://t.me/arvin_club',
    'VxUnderground': 'https://t.me/vxunderground',
    'Malpedia': 'https://t.me/malpedia',
    'LogsFree': 'https://t.me/locativelogsfree',
    'Darknet': 'https://t.me/dbforall',
    'GonjeshkeDarand': 'https://t.me/GonjeshkeDarand',
    'PryntStealer': 'https://t.me/officialpryntsoftware',
    'SiegedSec': 'https://t.me/SiegedSec',
    'BreachedForums': 'https://t.me/breached_co',
    'ArmyofThieves': 'https://t.me/ArmyThieves',
    'SharpBoys': 'https://t.me/sharpboys_3',
    'WLxDCONFIGS': 'https://t.me/WLxD_CRX',
    'TommyFlounder': 'https://t.me/floundertech',
    'GhostSec': 'https://t.me/GhostSecc',
    'ConfigMaster': 'https://t.me/config_combos',
    'Zer0DayLab': 'https://t.me/zer0daylab',
    'HADESSHOP': 'https://t.me/hadesh0p',
    'NoHideSpace': 'https://t.me/nohidespace',
    'KILLNET': 'https://t.me/killnet_reservs',
    'LOLZTEAM': 'https://t.me/lolz_guru',
    'Ares': 'https://t.me/aresmainchannel',
    'ZeroDayToday': 'https://t.me/LearnExploit',
    'CPartisan': 'https://t.me/cpartisans',
    'club1337': 'https://t.me/club1337',
    'Documentor': 'https://t.me/documentors',
    'DDoSecrets': 'https://t.me/AntiPlumbers',
    'SnatchTeam': 'https://t.me/snatch_news',
    'inj3ct0r': 'https://t.me/inj3ct0rs',
    'RalfHacker': 'https://t.me/RalfHackerChannel',
    'RuHeight': 'https://t.me/ruheight',
    'Data1eaks': 'https://t.me/data1eaks',
    'R0Crew': 'https://t.me/R0_Crew',
    'HeawsNet': 'https://t.me/heawsnet'
}


# Instatiate object per feed item
for feed in telegram_feed_list:
    vars()[feed] = telegram_client.get_entity(telegram_feed_list[feed])

    try: # TODO only join if not already joined
        telegram_client(JoinChannelRequest(vars()['feed']))
    except (UsernameInvalidError, TypeError, ValueError): # telegram user or channel was not found
        continue


"""
TODO test if this generic approch can replace repetitive code

@telegram_client.on(events.NewMessage(incoming=True))
async def event_handler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    for channel in telegram_feed_list:
        if channel.id == event.message.peer_id.channel_id:
            create_telegram_output(channel.title, event.message.message)
            break
"""


##****Arvin Group handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=ArvinGroup))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("Arvin Group", event.message.message)

##****vx-underground handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=VxUnderground))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("vx-underground", event.message.message)

##****Malpedia handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=Malpedia))
async def EventHandler(event):
    create_telegram_output("Malpedia", event.message.message)

##****LogsFree handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=LogsFree))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("LogsFree", event.message.message)
    
##****Darknet handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=Darknet))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("Darknet", event.message.message)
    
##****GonjeshkeDarand handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=GonjeshkeDarand))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("GonjeshkeDarand", event.message.message)
    
##****PryntStealer handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=PryntStealer))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("PryntStealer", event.message.message)
    
##****SiegedSec handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=SiegedSec))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("SiegedSec", event.message.message)

##****BreachedForums handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=BreachedForums))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("BreachedForums", event.message.message)
    
##****ArmyofThieves handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=ArmyofThieves))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("ArmyofThieves", event.message.message)

##****SharpBoys handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=SharpBoys))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("SharpBoys", event.message.message)

##****WLxDCONFIGS handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=WLxDCONFIGS))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("WLxDCONFIGS", event.message.message)
    
##****TommyFlounder handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=TommyFlounder))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("TommyFlounder", event.message.message)

##****GhostSec handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=GhostSec))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("GhostSec", event.message.message)
    
##****ConfigMaster handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=ConfigMaster))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("ConfigMaster", event.message.message)

##****Zer0DayLab handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=Zer0DayLab))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("Zer0DayLab", event.message.message)

##****HADESSHOP handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=HADESSHOP))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("HADESSHOP", event.message.message)

##****NoHideSpace handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=NoHideSpace))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("NoHideSpace", event.message.message)

##****KILLNET handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=KILLNET))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("KILLNET", event.message.message)

##****LOLZTEAM handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=LOLZTEAM))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("LOLZTEAM", event.message.message)

##****Ares handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=Ares))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("Ares", event.message.message)

##****ZeroDayToday handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=ZeroDayToday))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("ZeroDayToday", event.message.message)
    
##****CPartisan handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=CPartisan))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("CPartisan", event.message.message)
    
##****club1337 handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=club1337))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("club1337", event.message.message)
    
##****Documentor handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=Documentor))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("Documentor", event.message.message)
    
##****DDoSecrets handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=DDoSecrets))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("DDoSecrets", event.message.message)
    
##****SnatchTeam handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=SnatchTeam))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("SnatchTeam", event.message.message)
    
##****inj3ct0r handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=inj3ct0r))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("inj3ct0r", event.message.message)

##****RalfHacker handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=RalfHacker))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("RalfHacker", event.message.message)

##****RuHeight handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=RuHeight))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("RuHeight", event.message.message)

##****Data1eaks handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=Data1eaks))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("Data1eaks", event.message.message)

##****R0Crew handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=R0Crew))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("R0Crew", event.message.message)
    
##****HeawsNet handler****
@telegram_client.on(events.NewMessage(incoming=True,chats=HeawsNet))
async def EventHandler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    create_telegram_output("HeawsNet", event.message.message)


def create_telegram_output(group, message):
    telegram_feed.send(f'{group} {time.ctime()} {message}')
    

if __name__ == '__main__':
    telegram_client.run_until_disconnected()