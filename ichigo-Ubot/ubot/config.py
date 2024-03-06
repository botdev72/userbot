import os

from dotenv import load_dotenv

load_dotenv()

DEVS = [
    1014046713,
    1054295664,
    482945686,
    5021865183,
    1373315874,
    1351971763,
    750248553,
    5490512714,
    1021808828,
    ]
    
    
KYNAN = list(map(int, os.getenv("KYNAN", "1054295664 1202297638 1014046713 1923220086 482945686").split()))

API_ID = int(os.getenv("API_ID", "20410821"))

API_HASH = os.getenv("API_HASH", "be2f6e50fff466c53967c8d3484a2832")

BOT_TOKEN = os.getenv("BOT_TOKEN", "6862912862:AAFGrwqOApWgm9TYE1uQ_cgSCqcVljRneIY")

OWNER_ID = int(os.getenv("OWNER_ID", "1014046713"))

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "1054295664 1014046713 1923220086 482945686",
        ).split(),
    )
)

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1002112558277"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001608847572 -1001538826310 -1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001861414061 -1002133716625",
        ).split(),
    )
)

MAX_BOT = int(os.getenv("MAX_BOT", "25"))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "sky-osksnxjsiwjxjwosk",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://davv293:1234@cluster0.j1zsd2f.mongodb.net/?retryWrites=true&w=majority",
)
