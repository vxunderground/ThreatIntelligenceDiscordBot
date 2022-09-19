from configparser import ConfigParser, NoOptionError
from discord import Webhook, RequestsWebhookAdapter
from telethon import TelegramClient

from .Utils import verify_config_section

config = ConfigParser()
config.optionxform = str  # Preserve case when reading config file
config.read("config.ini")

for section in ["Webhooks", "Telegram"]:
    if not section in config:
        sys.exit(f'Please specify a "{section}" section in the config file')

    vars()[section.lower()] = None

if verify_config_section(config, "Webhooks"):
    webhooks = {
        hook_name: Webhook.from_url(hook_url, adapter=RequestsWebhookAdapter())
        for hook_name, hook_url in config.items("Webhooks")
    }

if verify_config_section(config, "Telegram"):
    telegram_client = TelegramClient(
        config["Telegram"]["BotName"],
        config["Telegram"]["APIID"],
        config["Telegram"]["APIHash"],
    )
