import os
import time
from discord import Webhook, RequestsWebhookAdapter, File
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
    try: # TODO consider only sending join requests if not already joined
        vars()[feed] = telegram_client.get_entity(telegram_feed_list[feed])
        telegram_client(JoinChannelRequest(vars()['feed']))
    except (UsernameInvalidError, TypeError, ValueError): # telegram user or channel was not found
        continue


@telegram_client.on(events.NewMessage(incoming=True))
async def event_handler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, 'rb'))
        telegram_feed.send(file=upload_file)
        
    for channel in telegram_feed_list:
        # TODO consider error handling here and write to a secondary discord status channel on errors
        try:
            if globals()[channel].id == event.message.peer_id.channel_id:
                create_telegram_output(globals()[channel].title, event.message.message)
                break
        except:
            continue


def create_telegram_output(group, message):
    telegram_feed.send(f'{group} {time.ctime()} {message}')
    

if __name__ == '__main__':
    telegram_client.run_until_disconnected()