# Threat Intelligence Discord Bot
The vx-underground Threat Intelligence Discord Bot gets updates from various clearnet domains and ransomware threat actor domains. This bot will check for updates in intervals of 1800 seconds.

* Written in Python 3.10 64bit
* Can run on Windows or Linux
* Requires Discord Webhook
* Easily add or remove domains wanting to be monitored
* Written by a C++ Windows programmer, variable and function naming convention will probably make you puke

# Getting Started
Step 1. Make a web hook. Not sure how to make a webhook? [Discord makes it easy!](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
Step 2. Create the config.txt file. This config.txt stores when data was recently updated. If a value has a "?" this means it has never received an update and/or is a new entry. The configuration file path is specified at the beginning of the python script.
Step 3. Have internet connection
Step 4. Run the script

# Adding or removing things to monitor
Step 1. All monitored RSS feeds are in the RssFeedList object. To add a new RSS feed simply append a new entry and assign it a config.txt file entry name. e.g.

```
["https://redcanary.com/feed/", "RedCanary"]
```
