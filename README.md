# Threat Intelligence Discord Bot
The vx-underground Threat Intelligence Discord Bot gets updates from various clearnet domains, ransomware threat actor domains, and Telegram channels. This bot will check for updates in intervals of 1800 seconds (omit Telegram bot).

* Written in Python 3.10 64bit
* Can run on Windows or Linux
* Requires Discord Webhook
* Easily add or remove domains wanting to be monitored
* Written by a C++ Windows programmer, variable and function naming convention will probably make you puke
* 2 Scripts are present, 1 is responsible for ransomware groups and clearnet domains. The other is responsible for handling Telegram channels.

# Getting Started
* Step 1. Make a web hook. Not sure how to make a webhook? [Discord makes it easy!](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
* Step 2. Create the config.txt file. This config.txt stores when data was recently updated. If a value has a "?" this means it has never received an update and/or is a new entry. The configuration file path is specified at the beginning of the python script.
* Step 2a. If you'd like to monitor Telegram channels, you will need a [Telegram API Key](https://core.telegram.org/api/obtaining_api_id)
* Step 3. Have internet connection
* Step 3a. If you're running the Telegram channel monitor, please note it downloads images from the Telegram channel. Sufficient hard disk space will be required to store images
* Step 4. Run the script

# Other notes
* By default this script requires 4 discord web hooks. It pipes output for private sector updates, governments updates, ransomware group updates, and log output to indicate whether or not it is running. Feel free to remove whatever, or add whatever
* Some Rss Feeds (such as Cybersecurity AT&T) have non-default RSS field keys. Some may require debugging to determine which fields are labeled as such. We simply removed these domains from the configuration file. We were too lazy to resolve this.
* There is no way to ensure what images are being posted to the Telegram channels. Proceed with caution
* This bot does not download attachments from Telegram channels. There is no way to determine what it is (reliably).


# Adding or removing RSS Feeds to monitor
All monitored RSS feeds are in the RssFeedList object. To add a new RSS feed simply append a new entry and assign it a config.txt file entry name. e.g.

In the Python script:
```
    RssFeedList = [["https://grahamcluley.com/feed/", "Graham Cluley"],
                   ["https://1337WebsiteIWannaFollow.com/feed/", "1337Website"]]
```

In the config file:
```
1337Website = ?
```
The "?" indicates it has never received an update.

# Adding or removing Telegram channels to monitor

* NOTE: The Telegram API is an ugly monster and does not make determining what is being filtered an easy task. This script contains A LOT of repetitive code. Perhaps clean it up and send a merge request? =D
* Step 1. Set the image download path in the python script && set the Discord web hook URL
* Step 2. Retrieve the Telegram channel entity via 
```
NewTelegramChannelName = TelegramClientObject.get_entity("https://t.me/TelegramChannelLink")
```
* Step 3. Send a join request when the application launches via 
```
TelegramClientObject(JoinChannelRequest(NewTelegramChannelName))
```
* Step 4. Set the Telegram async filter via
```
##****NewTelegramChannelName handler****
@TelegramClientObject.on(events.NewMessage(incoming=True,chats=NewTelegramChannelName))
async def EventHandler(EventObject):

    if EventObject.photo:
        ImageData = await EventObject.download_media(DownloadPath)
        UploadFile = discord.File(open(ImageData, 'rb'))
        TelegramFeed.send(file=UploadFile)
        
    CreateTelegramMessageOutput("NewTelegramChannelName", EventObject.message.message)
```
