import feedparser
import time
from configparser import ConfigParser
import requests
from discord import Webhook, RequestsWebhookAdapter
import urllib.request, json

ConfigurationFilePath = "C:\\Users\\User\\Documents\\config.txt" ##path to configuration file


FileConfig = ConfigParser()
FileConfig.read(ConfigurationFilePath)

PrivateSectorFeed = Webhook.from_url("https://discord.com/api/webhooks/000/000", adapter=RequestsWebhookAdapter()) ##private sector discord hook goes here
GovernmentFeed = Webhook.from_url("https://discord.com/api/webhooks/000/000", adapter=RequestsWebhookAdapter()) ##gov feed discord hook goes here
RansomwareFeed = Webhook.from_url("https://discord.com/api/webhooks/000/000", adapter=RequestsWebhookAdapter()) ##ransomware feed discord hook goes here
LogOutput = Webhook.from_url("https://discord.com/api/webhooks/000/000", adapter=RequestsWebhookAdapter()) ##logging channel discord hook goes here

def FnGetRansomwareUpdates():
    
    OutputString = ""

    with urllib.request.urlopen("https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json") as RansomwareUrl:
        Data = json.loads(RansomwareUrl.read().decode())
        for Entries in Data:

            DateActivity = Entries["discovered"]

            ###
            # No Need to create an entry in Config.txt 
            # by @JMousqueton               
            try:
                TmpObject = FileConfig.get('main', Entries["group_name"])
            except:
                FileConfig.set('main', Entries["group_name"], " = ?")
                TmpObject = FileConfig.get('main', Entries["group_name"])
           ###


            if "?" in TmpObject:
                FileConfig.set('main', Entries["group_name"], DateActivity)

            if(TmpObject >= DateActivity):
                continue
            else:
                FileConfig.set('main', Entries["group_name"], Entries["discovered"])
            
            OutputMessage = Entries["group_name"]
            OutputMessage += "\n"
            OutputMessage += Entries["discovered"]
            OutputMessage += "\n"
            OutputMessage += Entries["post_title"]

            RansomwareFeed.send(OutputMessage)
            time.sleep(3)

            FileConfig.set('main', Entries["group_name"], Entries["discovered"])

    with open(ConfigurationFilePath, 'w') as FileHandle:
        FileConfig.write(FileHandle)

def FnGetRssFromUrl(RssItem, HookChannelDesciptor):
    NewsFeed = feedparser.parse(RssItem[0])
    DateActivity = ""
    IsInitialRun = False

    LastSaved = FileConfig.get('main', RssItem[1])

    for RssObject in NewsFeed.entries:

        try:
            DateActivity = time.strftime('%Y-%m-%dT%H:%M:%S', RssObject.published_parsed)
        except: 
            DateActivity = time.strftime('%Y-%m-%dT%H:%M:%S', RssObject.updated_parsed)

        ###
        #  No Need to create an entry in Config.txt 
        # by @JMousqueton               
        try:
            TmpObject = FileConfig.get('main', RssItem[1])
        except:
            FileConfig.set('main', RssItem[1], " = ?")
            TmpObject = FileConfig.get('main', RssItem[1])    
        ### 
        
        if "?" in TmpObject:
            IsInitialRun = True
            FileConfig.set('main', RssItem[1], DateActivity)

        if IsInitialRun is False:
            if(TmpObject >= DateActivity):
                continue
            else:
                FileConfig.set('main', RssItem[1], DateActivity)
            
        OutputMessage = RssItem[1]
        OutputMessage += "\n"
        OutputMessage += "Date: " + DateActivity
        OutputMessage += "\n"
        OutputMessage += "Title: " + RssObject.title
        OutputMessage += "\n"
        OutputMessage += "Read more: " + RssObject.link
        OutputMessage += "\n"

        if HookChannelDesciptor == 1:
            PrivateSectorFeed.send(OutputMessage)

        if HookChannelDesciptor == 2:
            GovernmentFeed.send(OutputMessage)
            
        time.sleep(3)

    with open(ConfigurationFilePath, 'w') as FileHandle:
        FileConfig.write(FileHandle)

    IsInitialRun = False

def FnCreateLogStringAndWriteToDiscord(RssItem):
    LogString = "[*]" + time.ctime()
    LogString += " " + "checked " + RssItem
    LogOutput.send(LogString)
    time.sleep(2) 
    

def EntryMain():

    LogString = ""
    RssFeedList = [["https://grahamcluley.com/feed/", "Graham Cluley"],
                   ["https://threatpost.com/feed/", "Threatpost"],
                   ["https://krebsonsecurity.com/feed/", "Krebs on Security"],
                   ["https://www.darkreading.com/rss.xml", "Dark Reading"],
                   ["http://feeds.feedburner.com/eset/blog", "We Live Security"],
                   ["https://davinciforensics.co.za/cybersecurity/feed/", "DaVinci Forensics"],
                   ["https://blogs.cisco.com/security/feed", "Cisco"],
                   ["https://www.infosecurity-magazine.com/rss/news/", "Information Security Magazine"],
                   ["http://feeds.feedburner.com/GoogleOnlineSecurityBlog", "Google"],
                   ["http://feeds.trendmicro.com/TrendMicroResearch", "Trend Micro"],
                   ["https://www.bleepingcomputer.com/feed/", "Bleeping Computer"],
                   ["https://www.proofpoint.com/us/rss.xml", "Proof Point"],
                   ["http://feeds.feedburner.com/TheHackersNews?format=xml", "Hacker News"],
                   ["https://www.schneier.com/feed/atom/", "Schneier on Security"],
                   ["https://www.binarydefense.com/feed/", "Binary Defense"],
                   ["https://securelist.com/feed/", "Securelist"],
                   ["https://research.checkpoint.com/feed/", "Checkpoint Research"],
                   ["https://www.virusbulletin.com/rss", "VirusBulletin"],
                   ["https://modexp.wordpress.com/feed/", "Modexp"],
                   ["https://www.tiraniddo.dev/feeds/posts/default", "James Forshaw"],
                   ["https://blog.xpnsec.com/rss.xml", "Adam Chester"],
                   ["https://msrc-blog.microsoft.com/feed/", "Microsoft Security"],
                   ["https://www.recordedfuture.com/feed", "Recorded Future"],
                   ["https://www.sentinelone.com/feed/", "SentinelOne"],
                   ["https://redcanary.com/feed/", "RedCanary"],
                   ["https://cybersecurity.att.com/site/blog-all-rss", "ATT"]]
                   

    GovRssFeedList = [["https://www.cisa.gov/uscert/ncas/alerts.xml", "US-CERT CISA"],
                      ["https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml", "NCSC"],
                      ["https://www.cisecurity.org/feed/advisories", "Center of Internet Security"]]

    

    while(True):
            
        for RssItem in RssFeedList:
            FnGetRssFromUrl(RssItem, 1)
            FnCreateLogStringAndWriteToDiscord(RssItem[1])

        for GovRssItem in GovRssFeedList:
            FnGetRssFromUrl(GovRssItem, 2)
            FnCreateLogStringAndWriteToDiscord(GovRssItem[1])

        FnGetRansomwareUpdates()
        FnCreateLogStringAndWriteToDiscord("Ransomware TA List")

        time.sleep(1800)
                      
    
EntryMain()
    

    
