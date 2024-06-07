from logging import ERROR, INFO, FileHandler, StreamHandler, basicConfig, getLogger
from os import getenv
from time import time

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode
from uvloop import install

install()
basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",  #  [%(filename)s:%(lineno)d]
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)

getLogger("pyrogram").setLevel(ERROR)
getLogger("pymongo").setLevel(ERROR)
LOGGER = getLogger(__name__)

load_dotenv("config.env", override=True)
BOT_START = time()
bot_cache = {}

bot_chats = {
    -1002015038990: {
        "prices": {"1d": 10, "30d": 250, "90d": 600},
        "sshots": [
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
        ],
        "args": {"Type": "Games", "Desp": "Nothing to Say, Highly Recommended"},
    },    
   -1002093797403: {
        "prices": {"1y": 199,  "6m": 99},
        "sshots": [
            "https://telegra.ph/file/408c464aa15decb52d9eb.jpg",
            "https://telegra.ph/file/dbae82f39b64c55668e42.jpg",
            "https://telegra.ph/file/20de33383da6a864395aa.jpg",
        ],
        "args": {
            "Type": "Kannada videos",
            "Desp": "Nothing to Say, Highly Recommended kannada videos",
        },
    -1002127181784: {
        "prices": {"1d": 10, "30d": 28, "90d": 70},
        "sshots": [
            "https://te.legra.ph/file/e3aaee8624be55289c771.jpg",
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
        ],
        "args": {
            "Type": "test1",
            "Desp": "Nothing to Say, Highly Recommended with wide varieties",
        },
    },
}


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN", "7080709991:AAFXSt9i4k6OypBcPSd8KllkiucXR4_sMho")
    API_HASH = getenv("API_HASH", "7b93fc0adc30039f74a7faeba4a3875d")
    API_ID = getenv("API_ID", "20508620")
    if BOT_TOKEN == "" or API_HASH == "" or API_ID == "":
        LOGGER.critical("ENV Missing. Exiting Now...")
        exit(1)
    LOG_CHAT = int(getenv("LOG_CHAT", "-1002061267081"))
    ADMINS = list(map(int, getenv("ADMINS", "6059507751 6822467996 6971938312").split()))
    MONGODB_URL = getenv("MONGODB_URL", "mongodb+srv://kp9731818219:A6j4uZkfAhymgclV@cluster0.zanohyt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    AUTO_APPROVE = getenv("AUTO_APPROVE", "false").lower() == "true"
    REF_NEEDED = int(getenv("REF_NEEDED", "0"))

bot = Client(
    "Subs-Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="SubsManager/plugins"),
    parse_mode=ParseMode.HTML,
    workers=1000,
)
