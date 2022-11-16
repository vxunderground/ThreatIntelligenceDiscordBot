import os
import time
from discord import File

from telethon.sync import events, TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest

import logging
logger = logging.getLogger("telegram")

from .. import webhooks, config

image_download_path = os.path.join(
    os.getcwd(),
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
        logger.debug("Downloading image...")

        image_data = await event.download_media(os.path.join(image_download_path, str(event.photo.id)))
        with open(image_data, "rb") as upload_file:
            webhooks["TelegramFeed"].send(file=File(upload_file))

    create_telegram_output(event.chat.title, event.message.message)


def create_telegram_output(group, message):
    webhooks["TelegramFeed"].send(f"{group} {time.ctime()} {message}")


# Instatiate object per feed item
def init_client(client):
    for feed in telegram_feed_list.keys():
        try:  # TODO consider only sending join requests if not already joined
            logger.debug(f'Joining "{feed}" channel at {telegram_feed_list[feed]["url"]}')
            telegram_feed_list[feed]["channel"] = client.get_entity(telegram_feed_list[feed]["url"])
            client(JoinChannelRequest(telegram_feed_list[feed]["channel"]))
        except (
            UsernameInvalidError,
        ) as e:  # telegram user or channel was not found
            logger.warning(f'Problem when attempting to join "{feed}" channel at {telegram_feed_list[feed]["url"]}', exc_info=e)
            continue

    logger.debug("Registering event handler for handling new messages")
    client.add_event_handler(event_handler, events.NewMessage(incoming=True))


def main():
    with TelegramClient(
        config["Telegram"]["BotName"],
        config["Telegram"]["APIID"],
        config["Telegram"]["APIHash"],
    ) as client:
        logger.info("Initiating telegram client")
        init_client(client)
        client.run_until_disconnected()


if __name__ == "__main__":
    main()
