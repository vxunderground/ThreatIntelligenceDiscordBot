import os
import time
from discord import File

from telethon import events
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest

from .. import webhooks, config, telegram_client

image_download_path = os.path.join(
    os.getcwd(),
    "Source",
    config.get(
        "Telegram", "ImageDownloadFolder", raw=True, vars={"fallback": "TelegramImages"}
    ),
)

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

for name, url in telegram_feed_list.items():
    telegram_feed_list[name] = {"url" : url, "channel" : None}


async def event_handler(event):
    if event.photo:
        image_data = await event.download_media(image_download_path)
        upload_file = File(open(image_data, "rb"))
        webhooks["TelegramFeed"].send(file=upload_file)

    for feed in telegram_feed_list.keys():
        # TODO consider error handling here and write to a secondary discord status channel on errors
        try:
            if telegram_feed_list[feed]["channel"].id == event.message.peer_id.channel_id:
                create_telegram_output(telegram_feed_list[feed]["channel"].title, event.message.message)
                break
        except:
            continue


def create_telegram_output(group, message):
    webhooks["TelegramFeed"].send(f"{group} {time.ctime()} {message}")


# Instatiate object per feed item
def init():
    telegram_client.start()

    for feed in telegram_feed_list.keys():
        try:  # TODO consider only sending join requests if not already joined
            telegram_feed_list[feed]["channel"] = client.get_entity(telegram_feed_list[feed])
            client(JoinChannelRequest(telegram_feed_list[feed]["channel"]))
        except (
            UsernameInvalidError,
            TypeError,
            ValueError,
        ):  # telegram user or channel was not found
            continue

    telegram_client.add_event_handler(event_handler, events.NewMessage(incoming=True))


def main():
    init()
    telegram_client.run_until_disconnected()


if __name__ == "__main__":
    main()
