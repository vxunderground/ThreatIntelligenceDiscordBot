import sys

from . import config
from .Utils import get_missing_config_params


def verify_config(section_name):
    missing_params = get_missing_config_params(config, section_name)

    if len(missing_params) > 0:
        sys.exit(
            f"You havent't specified {', '.join(missing_params)} in the config.ini file"
        )


if __name__ == "__main__":
    verify_config("Webhooks")
    if len(sys.argv) > 1:
        match sys.argv[1].lower():
            case "discord":
                from .Bots import Discord as bot
            case "telegram":
                verify_config("Telegram")
                from .Bots import Telegram as bot
            case _:
                sys.exit(
                    "Argument not recognized. The possible options are discord and telegram"
                )

        bot.main()
    else:
        sys.exit(
            "Please provide an argument for what bot should be run. The possible options are discord and telegram"
        )
