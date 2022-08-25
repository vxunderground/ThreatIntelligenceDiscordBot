import json
import os
import requests
import time
from enum import Enum

import signal
import sys
import atexit

import feedparser
from configparser import ConfigParser, NoOptionError
from discord import Webhook, RequestsWebhookAdapter

from Formatting import format_single_article

# expects the configuration file in the same directory as this script by default, replace if desired otherwise
configuration_file_path = os.path.join(
    os.path.split(os.path.abspath(__file__))[0], "Config.txt"
)

# put the discord hook urls to the channels you want to receive feeds in here
private_sector_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
government_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
ransomware_feed = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())
# this one is logging of moniotring status only
status_messages = Webhook.from_url('https://discord.com/api/webhooks/000/000', adapter=RequestsWebhookAdapter())

private_rss_feed_list = [
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
    ["https://www.cisa.gov/uscert/ncas/alerts.xml", "US-CERT CISA"],
    ["https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml", "NCSC"],
    ["https://www.cisecurity.org/feed/advisories", "Center of Internet Security"],
]

FeedTypes = Enum("FeedTypes", "RSS JSON")

source_details = {
    "Private RSS Feed": {
        "source": private_rss_feed_list,
        "hook": private_sector_feed,
        "type": FeedTypes.RSS,
    },
    "Gov RSS Feed": {
        "source": gov_rss_feed_list,
        "hook": government_feed,
        "type": FeedTypes.RSS,
    },
    "Ransomware News": {
        "source": "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json",
        "hook": ransomware_feed,
        "type": FeedTypes.JSON,
    },
}


config_file = ConfigParser()
config_file.read(configuration_file_path)


def get_ransomware_news(source):
    posts = requests.get(source).json()

    for post in posts:
        post["publish_date"] = post["discovered"]
        post["title"] = "Post: " + post["post_title"]
        post["source"] = post["group_name"]

    return posts


def get_news_from_rss(rss_item):
    feed_entries = feedparser.parse(rss_item[0]).entries

    # This is needed to ensure that the oldest articles are proccessed first. See https://github.com/vxunderground/ThreatIntelligenceDiscordBot/issues/9 for reference
    for rss_object in feed_entries:
        rss_object["source"] = rss_item[1]
        try:
            rss_object["publish_date"] = time.strftime(
                "%Y-%m-%dT%H:%M:%S", rss_object.published_parsed
            )
        except:
            rss_object["publish_date"] = time.strftime(
                "%Y-%m-%dT%H:%M:%S", rss_object.updated_parsed
            )

    return feed_entries


def proccess_articles(articles):
    messages, new_articles = [], []
    articles.sort(key=lambda article: article["publish_date"])

    for article in articles:
        try:
            config_entry = config_file.get("main", article["source"])
        except NoOptionError:  # automatically add newly discovered groups to config
            config_file.set("main", article["source"], " = ?")
            config_entry = config_file.get("main", article["source"])

        if config_entry.endswith("?"):
            config_file.set("main", article["source"], article["publish_date"])
        else:
            if config_entry >= article["publish_date"]:
                continue

        messages.append(format_single_article(article))
        new_articles.append(article)

    return messages, new_articles


def send_messages(hook, messages, articles, batch_size=10):
    for i in range(0, len(messages), batch_size):
        hook.send(embeds=messages[i : i + batch_size])

        for article in articles[i : i + batch_size]:
            config_file.set(
                "main", article["source"], article["publish_date"]
            )

        time.sleep(3)


def process_source(post_gathering_func, source, hook):
    raw_articles = post_gathering_func(source)

    processed_articles, new_raw_articles = proccess_articles(raw_articles)
    send_messages(hook, processed_articles, new_raw_articles)


def handle_rss_feed_list(rss_feed_list, hook):
    for rss_feed in rss_feed_list:
        status_messages.send(f"> {rss_feed[1]}")
        process_source(get_news_from_rss, rss_feed, hook)


def write_status_messages_to_discord(message):
    status_messages.send(f"**{time.ctime()}**: *{message}*")
    time.sleep(3)


@atexit.register
def clean_up_and_close():
    with open(configuration_file_path, "w") as f:
        config_file.write(f)

    sys.exit(0)


def main():
    while True:
        for detail_name, details in source_details.items():
            write_status_messages_to_discord(f"Checking {detail_name}")

            if details["type"] == FeedTypes.JSON:
                process_source(get_ransomware_news, details["source"], details["hook"])
            elif details["type"] == FeedTypes.RSS:
                handle_rss_feed_list(details["source"], details["hook"])

        write_status_messages_to_discord("All done")
        with open(configuration_file_path, "w") as f:
            config_file.write(f)

        time.sleep(1800)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda num, frame: clean_up_and_close())
    main()
