from configparser import ConfigParser, NoOptionError
from discord import Webhook, RequestsWebhookAdapter
from telethon import TelegramClient

config = ConfigParser()
config.optionxform = str  # Preserve case when reading config file
config.read("config.ini")

webhooks = None
telegram_client = None


def verify_config_section(section_name):
    return section_name in config and all(
        [detail for detail_name, detail in config.items(section_name)]
    )


if verify_config_section("Webhooks"):
    webhooks = {
        hook_name: Webhook.from_url(hook_url, adapter=RequestsWebhookAdapter())
        for hook_name, hook_url in config.items("Webhooks")
    }

if verify_config_section("Telegram"):
    telegram_client = TelegramClient(
        config["Telegram"]["BotName"],
        config["Telegram"]["APIID"],
        config["Telegram"]["APIHash"],
    )
