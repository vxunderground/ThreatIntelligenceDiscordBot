import feedparser
import json
import os
import requests
import time
from configparser import ConfigParser, NoOptionError
from discord import Webhook, RequestsWebhookAdapter

from Formatting import format_single_article

# expects the configuration file in the same directory as this script by default, replace if desired otherwise
configuration_file_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'Config.txt')

# put the discord hook urls to the channels you want to receive feeds in here
private_sector_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
government_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
ransomware_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
# this one is logging of moniotring status only
status_messages = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())

rss_feed_list = [
    ['https://grahamcluley.com/feed/', 'Graham Cluley'],
    ['https://threatpost.com/feed/', 'Threatpost'],
    ['https://krebsonsecurity.com/feed/', 'Krebs on Security'],
    ['https://www.darkreading.com/rss.xml', 'Dark Reading'],
    ['http://feeds.feedburner.com/eset/blog', 'We Live Security'],
    ['https://davinciforensics.co.za/cybersecurity/feed/', 'DaVinci Forensics'],
    ['https://blogs.cisco.com/security/feed', 'Cisco'],
    ['https://www.infosecurity-magazine.com/rss/news/', 'Information Security Magazine'],
    ['http://feeds.feedburner.com/GoogleOnlineSecurityBlog', 'Google'],
    ['http://feeds.trendmicro.com/TrendMicroResearch', 'Trend Micro'],
    ['https://www.bleepingcomputer.com/feed/', 'Bleeping Computer'],
    ['https://www.proofpoint.com/us/rss.xml', 'Proof Point'],
    ['http://feeds.feedburner.com/TheHackersNews?format=xml', 'Hacker News'],
    ['https://www.schneier.com/feed/atom/', 'Schneier on Security'],
    ['https://www.binarydefense.com/feed/', 'Binary Defense'],
    ['https://securelist.com/feed/', 'Securelist'],
    ['https://research.checkpoint.com/feed/', 'Checkpoint Research'],
    ['https://www.virusbulletin.com/rss', 'VirusBulletin'],
    ['https://modexp.wordpress.com/feed/', 'Modexp'],
    ['https://www.tiraniddo.dev/feeds/posts/default', 'James Forshaw'],
    ['https://blog.xpnsec.com/rss.xml', 'Adam Chester'],
    ['https://msrc-blog.microsoft.com/feed/', 'Microsoft Security'],
    ['https://www.recordedfuture.com/feed', 'Recorded Future'],
    ['https://www.sentinelone.com/feed/', 'SentinelOne'],
    ['https://redcanary.com/feed/', 'RedCanary'],
    ['https://cybersecurity.att.com/site/blog-all-rss', 'ATT']
]

gov_rss_feed_list = [
    ['https://www.cisa.gov/uscert/ncas/alerts.xml', 'US-CERT CISA'],
    ['https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml', 'NCSC'],
    ['https://www.cisecurity.org/feed/advisories', 'Center of Internet Security']
]

config_file = ConfigParser()
config_file.read(configuration_file_path)


def get_ransomware_updates():
    r = requests.get('https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json')

    for entries in r.json():
        date_activity = entries['discovered']

        try:
            config_entry = config_file.get('main', entries['group_name'])
        except NoOptionError: # automatically add newly discovered groups to config
            config_file.set('main', entries["group_name"], " = ?")
            config_entry = config_file.get('main', entries["group_name"])

        if config_entry.endswith('?'):
            config_file.set('main', entries['group_name'], date_activity)

        if(config_entry >= date_activity): # TODO this works but is probably not the best way to handle datetimes
            continue
        else:
            config_file.set('main', entries['group_name'], entries['discovered'])
        
        message = f'{entries["group_name"]}\n{entries["discovered"]}\n{entries["post_title"]}'
        ransomware_feed.send(message)
        time.sleep(3)

        config_file.set('main', entries['group_name'], entries['discovered'])

    with open(configuration_file_path, 'w') as f:
        config_file.write(f)


def get_rss_from_url(rss_item, hook_channel_descriptor):
    feed_entries = feedparser.parse(rss_item[0]).entries
    messages = []

    # This is needed to ensure that the oldest articles are proccessed first. See https://github.com/vxunderground/ThreatIntelligenceDiscordBot/issues/9 for reference
    for rss_object in feed_entries:
        try:
            rss_object["publish_date"] = time.strftime('%Y-%m-%dT%H:%M:%S', rss_object.published_parsed)
        except:
            rss_object["publish_date"] = time.strftime('%Y-%m-%dT%H:%M:%S', rss_object.updated_parsed)

    feed_entries.sort(key=lambda rss_object:rss_object["publish_date"])

    # Only take the latest 10, as this is more than enough given the half an hour interval the script is run at, and discord can't send more than 10 embedded messages at once
    for rss_object in feed_entries[-10:]:
        try:
            config_entry = config_file.get('main', rss_item[1])
        except NoOptionError: # automatically add newly discovered groups to config
            config_file.set('main', rss_item[1], " = ?")
            config_entry = config_file.get('main', rss_item[1])   

        if config_entry.endswith('?'):
            config_file.set('main', rss_item[1], rss_object["publish_date"])
        else:
            if(config_entry >= rss_object["publish_date"]):
                continue
            else:
                config_file.set('main', rss_item[1], rss_object["publish_date"])

        messages.append(format_single_article(rss_item[1], rss_object))

    if messages:
        if hook_channel_descriptor == 1:
            private_sector_feed.send(embeds=messages)
        elif hook_channel_descriptor == 2:
            government_feed.send(embeds=messages)
        else:
            pass


    with open(configuration_file_path, 'w') as f:
        config_file.write(f)


def write_status_messages_to_discord(rss_item):
    status_messages.send(f'[*]{time.ctime()} checked {rss_item}')
    time.sleep(2) 


if __name__ == '__main__':
    while(True):
        for rss_item in rss_feed_list:
            get_rss_from_url(rss_item, 1)
            write_status_messages_to_discord(rss_item[1])
            time.sleep(3) # To avoid rate limiting

        for rss_item in gov_rss_feed_list:
            get_rss_from_url(rss_item, 2)
            write_status_messages_to_discord(rss_item[1])
            time.sleep(3) # To avoid rate limiting

        get_ransomware_updates()
        write_status_messages_to_discord('Ransomware TA List')

        time.sleep(1800)