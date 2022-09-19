import sys
from .Bots import Discord, Telegram

if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "discord":
                Discord.main()
            case "telegram":
                Telegram.main()
    else:
        print("Please provide an argument for what bot should be run")
