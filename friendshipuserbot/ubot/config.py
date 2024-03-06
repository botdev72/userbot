import os
from dotenv import load_dotenv

load_dotenv()

DEVS = [
    1225177634,
    1054295664,
    5063062493,
    6002994221,
    2073506739,
    2033762302,
    793488327,
    5357942628,
    5013987239,
    876054262,
    482945686,
    1373744866,
    1839010591,
    816526222,  # lucifer
    1860375797,  # iamuput><
    961659670,  # kazuajgemang
    750233563,
    1736494994,  # nakakontol
    745256666,
    1202297638,
]

KYNAN = list(
    map(
        int,
        os.getenv(
            "KYNAN",
            "1225177634 6314633791 6508357237 482945686",
        ).split(),
    )
)

API_ID = int(os.getenv("API_ID", "20783349"))

API_HASH = os.getenv("API_HASH", "ca6822288826f84ade23f7a097c0281c")

BOT_TOKEN = os.getenv("BOT_TOKEN", "6714417739:AAFncIKnuj-ez4e-23Po-tEn9CN4DdFwLdA")

OWNER_ID = int(os.getenv("OWNER_ID", "1225177634"))

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "1225177634 6314633791 6508357237 1310165148",
        ).split(),
    )
)

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1001977284707"))

LOG_SELLER = int(os.getenv("LOG_SELLER", "-4006807112"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001794660377 -1001759323059 -4006807112 -1002094957966 -1002106238548 -1001908722151 -1001812143750",
        ).split(),
    )
)

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "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",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://pakdheubot:123123abc@cluster0.ebhjwzs.mongodb.net/?retryWrites=true&w=majority",
)

DB_NAME = os.getenv("DB_NAME", "mongo.skyubot")