from discord import Embed

from datetime import datetime
import dateutil.parser


MAIN_COLOR = 0x000000


def cut_string(string, length):
    return (string[: (length - 3)].strip() + "...") if len(string) > length else string


def format_datetime(article_datetime):
    if not isinstance(article_datetime, datetime):
        try:
            article_datetime = dateutil.parser.isoparse(article_datetime)
        except ValueError:
            return article_datetime.split("T")

    return [article_datetime.strftime("%d, %b %Y"), article_datetime.strftime("%H:%M")]


def format_single_article(source, article):
    description = ""

    if "summary" in article:
        for text_part in article["summary"].split("."):
            if not (len(description) + len(text_part)) > 250:
                description += text_part + "."
            else:
                description += ".."
                break

    source_text = f"**Source**: *{source}*"
    date_text = (
        "**Date**: " + " | *".join(format_datetime(article["publish_date"])) + "*"
    )

    if "link" in article:
        message = Embed(
            title=article["title"],
            url=article["link"],
            color=MAIN_COLOR,
        )
    else:
        message = Embed(
            title=article["title"],
            color=MAIN_COLOR,
        )

    if description and "link" in article:
        message.add_field(name=description, value=article["link"], inline=False)

        message.add_field(
            name="Details: ",
            value=source_text + "\n" + date_text,
            inline=False,
        )

    else:
        message.add_field(
            name=source_text,
            value=date_text,
            inline=False,
        )

    return message
