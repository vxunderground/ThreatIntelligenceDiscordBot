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

    message = Embed(
        title=article["title"],
        url=article["link"],
        color=MAIN_COLOR,
    )

    if description:
        message.add_field(name=description, value=article["link"], inline=False)

    message.add_field(
        name="Details: ",
        value="**Source:** "
        + source
        + "\n"
        + "**Date:** "
        + " | *".join(format_datetime(article["publish_date"]))
        + "*",
        inline=False,
    )
    return message
