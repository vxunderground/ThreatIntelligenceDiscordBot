import json
import os
import requests
import time
from enum import Enum

import signal
import sys
import atexit

import logging

logger = logging.getLogger("rss")

import feedparser
from configparser import ConfigParser, NoOptionError

from .. import webhooks, config
from ..Formatting import format_single_article

from datetime import datetime, timedelta

START_DATETIME = datetime(2024, 1, 30)  # articles before this datetime are not posted
DATETIME_FORMAT_RANSOMWARE = "%Y-%m-%d %H:%M:%S.%f"  # assumed datetime format of all articles
DATETIME_FORMAT_NEWS = "%Y-%m-%dT%H:%M:%S"
DATETIME_FORMAT_ISO = "%Y-%m-%dT%H:%M:%S.%f"
VERBOSE_DISCORD_POSTING = False
CVE_SOURCE = "NIST"
# TODO: add CVE API queries.
# https://nvd.nist.gov/developers/vulnerabilities
# pubStartDate & pubEndDate are useful parameters
# Something like:
# https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate=2021-08-04T00:00:00.000&pubEndDate=2021-10-22T00:00
# :00.000

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

FeedTypes = Enum("FeedTypes", "RSS JSON CVEAPI")

source_details = {
    "Private RSS Feed": {
        "source": private_rss_feed_list,
        "hook"  : webhooks["PrivateSectorFeed"],
        "type"  : FeedTypes.RSS,
    },
    "Gov RSS Feed"    : {
        "source": gov_rss_feed_list,
        "hook"  : webhooks["GovermentFeed"],
        "type"  : FeedTypes.RSS,
    },
    "Ransomware News" : {
        "source": "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json",
        "hook"  : webhooks["RansomwareFeed"],
        "type"  : FeedTypes.JSON,
    },
    "CVE News"        : {
        "source": "",  # no source because API needs start and end date time for query
        "hook"  : webhooks["CVEFeed"],
        "type"  : FeedTypes.CVEAPI,
    },
}

rss_log_file_path = os.path.join(
    os.getcwd(),
    "Source",
    config.get("RSS", "RSSLogFile", raw=True, vars={"fallback": "RSSLog.txt"}),
)

rss_log = ConfigParser()
rss_log.read(rss_log_file_path)


def get_ransomware_news(source):
    logger.debug("Querying latest ransomware information")
    posts = requests.get(source).json()
    for post in posts:
        post["publish_date"] = post["discovered"]
        post["title"] = "Post: " + post["post_title"]
        post["source"] = post["group_name"]
    return posts


def get_nist_cve_between(dt_start_utc, dt_end_utc):
    """
    See https://nvd.nist.gov/developers/vulnerabilities on API details
    dt_start_utc: datetime object indicating earliest date-time to query, e.g. datetime.utcnow()
    dt_end_utc: datetime object indicating latest date-time to query
    returns: List of dict
    dict has keys: ['id': str, 'source': str ("NIST"), 'source_id': str, 'publish_date': str, 'vuln_status': str,
    'description': str]
    date_published is ISO-8601 format, example: '2024-01-28T23:15:58.350'
    """
    # assert isinstance(dt_start_utc, datetime.datetime)
    # assert isinstance(dt_end_utc, datetime.datetime)
    url_request = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate=" \
                  f"{dt_start_utc.isoformat()}&pubEndDate={dt_end_utc.isoformat()}"
    logger.debug(f"Querying NIST CVE API: {url_request}")
    response = requests.get(url_request)
    cves = []
    if response.status_code == 200:
        response_json = response.json()
        if ("vulnerabilities" not in response_json) or not isinstance(response_json["vulnerabilities"], list):
            logger.critical(f"NIST CVE query JSON does not contain key 'vulnerabilities' or is not type of list")
            return cves
        for cve_dict in response_json["vulnerabilities"]:
            cve_dict = cve_dict["cve"]
            cve_id = cve_dict["id"]
            cve_source_id = cve_dict["sourceIdentifier"]
            cve_date_published = cve_dict["published"]
            cve_vuln_status = cve_dict["vulnStatus"]
            cve_link = "https://nvd.nist.gov/vuln/detail/" + cve_id
            cve_description = None
            for description in cve_dict["descriptions"]:
                if description["lang"] == "en":
                    cve_description = description["value"]
                    break
            if cve_description is None:
                cve_description = "N/A in English"
            cve = dict()
            cve["id"] = cve_id
            cve["link"] = cve_link
            cve["source"] = CVE_SOURCE
            cve["source_id"] = cve_source_id
            cve[
                "publish_date"] = cve_date_published  # change to uniformly used "publish_date" from NIST-specific
            # "date_published" key
            cve["vuln_status"] = cve_vuln_status
            cve["description"] = cve_description
            cves.append(cve)
    else:
        logger.critical(f"NIST query failed with status code {response.status_code}.")
    return cves


def get_new_nist_cve(source):
    # TODO: this only queries from the last 7 days (~500 results in one test try). If more flexibility
    #  required, need to implement the handling of multiple possible pages (limit: 2000 results/page). See
    #  resultsPerPage under https://nvd.nist.gov/developers/vulnerabilities
    # source: dummy variable, as right now only NIST is allowed as source.
    dt_end_utc = datetime.utcnow()
    dt_start_utc = dt_end_utc - timedelta(days=7)
    cves = get_nist_cve_between(dt_start_utc, dt_end_utc)
    return cves


def get_news_from_rss(rss_item):
    logger.debug(f"Querying RSS feed at {rss_item[0]}")
    feed_entries = feedparser.parse(rss_item[0]).entries
    feed_entries_filtered = []
    # This is needed to ensure that the oldest articles are proccessed first. See
    # https://github.com/vxunderground/ThreatIntelligenceDiscordBot/issues/9 for reference
    for rss_object in feed_entries:
        rss_object["source"] = rss_item[1]
        try:
            rss_object["publish_date"] = time.strftime(
                DATETIME_FORMAT_NEWS, rss_object.published_parsed
            )
        except:
            rss_object["publish_date"] = time.strftime(
                DATETIME_FORMAT_NEWS, rss_object.updated_parsed
            )
    return feed_entries


def process_articles(articles):
    messages, new_articles = [], []
    articles.sort(key=lambda article: article["publish_date"])
    for article in articles:
        try:
            config_entry = rss_log.get("main", article["source"])
        except NoOptionError:  # automatically add newly discovered groups to config
            rss_log.set("main", article["source"], " = ?")
            config_entry = rss_log.get("main", article["source"])

        if config_entry.endswith("?"):
            rss_log.set("main", article["source"], article["publish_date"])
        else:
            if config_entry >= article["publish_date"]:
                continue
        # TODO: unify timedate formats!
        # Global earliest time point filtering
        try:  # format of ransomware feed
            article_publish_date = datetime.strptime(article["publish_date"], DATETIME_FORMAT_RANSOMWARE)
        except ValueError as e:
            try:  # format of rest of RSS
                article_publish_date = datetime.strptime(article["publish_date"], DATETIME_FORMAT_NEWS)
            except ValueError as e2:
                # format of NIST API datetime strings
                article_publish_date = datetime.strptime(article["publish_date"], DATETIME_FORMAT_ISO)
        if article_publish_date >= START_DATETIME:
            messages.append(format_single_article(article))
            new_articles.append(article)

    return messages, new_articles


def send_messages(hook, messages, articles, batch_size=10):
    logger.debug(f"Sending {len(messages)} messages in batches of {batch_size}")
    for i in range(0, len(messages), batch_size):
        hook.send(embeds=messages[i: i + batch_size])

        for article in articles[i: i + batch_size]:
            rss_log.set("main", article["source"], article["publish_date"])

        time.sleep(3)


def process_source(post_gathering_func, source):
    raw_articles = post_gathering_func(source)
    processed_articles, new_raw_articles = process_articles(raw_articles)
    return processed_articles, new_raw_articles


def handle_rss_feed_list(rss_feed_list, hook):
    for rss_feed in rss_feed_list:
        logger.info(f"Handling RSS feed for {rss_feed[1]}")
        processed_articles, new_raw_articles = process_source(get_news_from_rss, rss_feed)
        if VERBOSE_DISCORD_POSTING or len(processed_articles) > 0:
            webhooks["StatusMessages"].send(f"> {rss_feed[1]}")
        send_messages(hook, processed_articles, new_raw_articles)


def write_status_message(message):
    webhooks["StatusMessages"].send(f"**{time.ctime()}**: *{message}*")
    logger.info(message)


def clean_up_and_close():
    logger.critical("Writing last things to rss log file and closing up")
    with open(rss_log_file_path, "w") as f:
        rss_log.write(f)

    sys.exit(0)


def main():
    logger.debug("Registering clean-up handlers")
    atexit.register(clean_up_and_close)
    signal.signal(signal.SIGTERM, lambda num, frame: clean_up_and_close())

    while True:
        for detail_name, details in source_details.items():
            if VERBOSE_DISCORD_POSTING:
                write_status_message(f"Checking {detail_name}")
            if details["type"] == FeedTypes.JSON:
                processed_articles, new_raw_articles = process_source(get_ransomware_news, details["source"])
                if VERBOSE_DISCORD_POSTING or len(processed_articles) > 0:
                    webhooks["StatusMessages"].send(f"> Ransomware News")
                send_messages(details["hook"], processed_articles, new_raw_articles)
            elif details["type"] == FeedTypes.RSS:
                handle_rss_feed_list(details["source"], details["hook"])
            elif details["type"] == FeedTypes.CVEAPI:  # data is gathered using function get_new_nist_cve()
                processed_articles, new_raw_articles = process_source(get_new_nist_cve, CVE_SOURCE)
                if VERBOSE_DISCORD_POSTING or len(processed_articles) > 0:
                    webhooks["StatusMessages"].send(f"> CVEs")
                send_messages(details["hook"], processed_articles, new_raw_articles)
            time.sleep(3)
        # Update RSS log
        logger.debug("Writing new time to rss log file")
        with open(rss_log_file_path, "w") as f:
            rss_log.write(f)
        if VERBOSE_DISCORD_POSTING:
            write_status_message("All done, going to sleep")
        else:
            logger.info("All done, going to sleep")

        time.sleep(1800)


if __name__ == "__main__":
    main()
