import os

from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [
    1054295664, #keenan
    482945686, #keenan2
    1860375797, #iamuput
    1988690500, #anara
    712277262, #iamuput2
    5063062493, #kazu
    961659670, #kazu2
    1992087933, #xenn
    1329377873, #xenn2
    2073495031, #piki
    5170630278, #pikianjing
    479344690, #ray
    5569311686, #rewe
    1087819304, #reza
]

KYNAN = list(map(int, os.getenv("KYNAN", "1054295664 1860375797 712277262 1988690500").split()))

API_ID = int(os.getenv("API_ID", "28358285"))

API_HASH = os.getenv("API_HASH", "8930157ab19270574cd27b89f215d49a")

BOT_TOKEN = os.getenv("BOT_TOKEN", "6351345147:AAG_9q1kvoQ0Cf2-Xrmk7jlaw7S4YYM0qYY")

OWNER_ID = int(os.getenv("OWNER_ID", "1860375797"))

USER_ID = list(map(int, os.getenv("USER_ID", "1860375797 1988690500 712277262").split()))

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1001933717453"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001608847572 -1001982790377 -1001538826310 -1001861414061").split()))

MAX_BOT = int(os.getenv("MAX_BOT", "50"))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "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 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",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://uputra:uputra@cluster0.n94m27s.mongodb.net/?retryWrites=true&w=majority",
)
