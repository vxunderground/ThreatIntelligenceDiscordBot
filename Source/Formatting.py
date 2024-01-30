from discord import Embed

from datetime import datetime
import dateutil.parser

MAIN_COLOR = 0x000000
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/87911852?s=280&v=4"


def cut_string(string, length):
    return (string[: (length - 3)].strip() + "...") if len(string) > length else string


def format_datetime(article_datetime):
    if not isinstance(article_datetime, datetime):
        try:
            article_datetime = dateutil.parser.isoparse(article_datetime)
        except ValueError:
            return article_datetime.split("T")

    return [article_datetime.strftime("%d, %b %Y"), article_datetime.strftime("%H:%M")]


def format_single_article(article):
    description = ""

    if "summary" in article:
        for text_part in article["summary"].split("."):
            if not (len(description) + len(text_part)) > 256:
                description += text_part + "."
            else:
                description += ".."
                break
    elif "description" in article:
        description = article["description"]
        if len(description) > 2048:  # Embed descriptions are limited to 2048 in Discord API
            description = description[:2045] + "..."
    if "source_id" in article:
        source_text = f"**Source**: *{article['source']} | {article['source_id']}*"
    else:
        source_text = f"**Source**: *{article['source']}*"

    date_text = (
            "**Date**: " + " | *".join(format_datetime(article["publish_date"])) + "*"
    )
    if "title" in article:
        title = article["title"]
    elif "id" in article:
        title = article["id"]
    if "link" in article:
        message = Embed(
            title=title,
            url=article["link"],
            color=MAIN_COLOR,
        )
    else:
        message = Embed(
            title=title,
            color=MAIN_COLOR,
        )

    if description:
        if "link" in article:
            message.add_field(name="Description", value=description, inline=False)
            details_field_value =source_text + "\n" + date_text
            if "vuln_status" in article:  # if vulnerability status available (for CVE), append to details
                details_field_value += "\n"
                details_field_value += f"**Status:** {article['vuln_status']}"
            message.add_field(
                name="Details: ",
                value= details_field_value,
                inline=False,
            )
    else:
        if title:
            message.set_thumbnail(url=THUMBNAIL_URL)

        message.add_field(
            name=source_text,
            value=date_text,
            inline=False,
        )
    return message