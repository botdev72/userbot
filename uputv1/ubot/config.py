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

KYNAN = list(map(int, os.getenv("KYNAN", "1054295664 1860375797 712277262").split()))

API_ID = int(os.getenv("API_ID", "17250424"))

API_HASH = os.getenv("API_HASH", "753bc98074d420ef57ddf7eb1513162b")

BOT_TOKEN = os.getenv("BOT_TOKEN", "6560233633:AAEvCQv7YDsMMFdWTAsjBJmmg143MlR226E")

OWNER_ID = int(os.getenv("OWNER_ID", "1860375797"))

USER_ID = list(map(int, os.getenv("USER_ID", "1860375797 712277262").split()))

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1001682195874"))

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1001682195874"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001608847572 -1001982790377 -1001538826310 -1001861414061 -1001876092598").split()))

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "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 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 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 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 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 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",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://uputra:uputra@cluster0.n94m27s.mongodb.net/?retryWrites=true&w=majority",
)
