from configparser import ConfigParser, NoOptionError
from discord import Webhook, RequestsWebhookAdapter

from .Utils import verify_config_section

from os import mkdir

# Need to create folder before running script, as the logger will otherwise throw error
try:
    mkdir("logs")
except OSError:
    pass # Most likely simply means the folder already exists

config = ConfigParser()
config.optionxform = str  # Preserve case when reading config file
config.read("config.ini")

for section in ["Webhooks", "Telegram"]:
    if not section in config:
        sys.exit(f'Please specify a "{section}" section in the config file')

if verify_config_section(config, "Webhooks"):
    webhooks = {
        hook_name: Webhook.from_url(hook_url, adapter=RequestsWebhookAdapter())
        for hook_name, hook_url in config.items("Webhooks")
    }
