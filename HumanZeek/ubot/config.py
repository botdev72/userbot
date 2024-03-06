import os

from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [
   1637576534
]


API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1001608847572 -1001538826310 -1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001861414061").split()))

OPENAI_API = os.environ.get("OPENAI_API", "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")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

OWNER_ID = int(os.environ.get("OWNER_ID", "1637576534"))

MAX_BOT = int(os.environ.get("MAX_BOT", "30"))

SKY = int(os.environ.get("SKY", ""))

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "",
)
