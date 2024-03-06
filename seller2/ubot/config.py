import os

from dotenv import load_dotenv

load_dotenv()


DEVS = [
    1054295664, #keenan
    482945686, #keenan2
    1860375797, #iamuput
    712277262, #iamuput2
    5063062493, #kazu
    817945139, #kazu2
    1992087933, #xenn
    1329377873, #xenn2
    2073495031, #piki
    5170630278, #pikianjing
    479344690, #ray
    5569311686, #rewe
    1087819304, #reza
    1736494994, #nakakontol
    816526222, #lucientod
]

KYNAN = list(
    map(
        int,
        os.getenv(
            "KYNAN",
            "482945686 1054295664 1860375797 712277262 816526222",
        ).split(),
    )
)

API_ID = int(os.getenv("API_ID", "17250424"))

API_HASH = os.getenv("API_HASH", "753bc98074d420ef57ddf7eb1513162b")

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1001933717453"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001608847572 -1001982790377 -1001538826310 -1001861414061 -1001876092598",
        ).split(),
    )
)

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "482945686 1860375797 712277262 816526222",
        ).split(),
    )
)

OPENAI_KEY = os.getenv(
    "OPENAI_KEY", "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"
)


BOT_TOKEN = os.getenv(
    "BOT_TOKEN", "6619582536:AAFm3be-Hl7EwXJyk4VsIgkZJKbKFzs8gf4"
)

BOT_SESSION = os.getenv(
    "BOT_SESSION",
    "BQEHOHgAke1bi7kaQfbez969ghcs72y27l8T8WiESQ0WIzPzwnAwLRqPDiHchcXv6holG6QFs2iIBEiF6qJFn350tJfgKELNWJAWhzJCXPcb1Yd9SBtb7361a-cEhE5F81mIEbeAmhb5QMovJEW7aGV9HAdl1_jiSdrvqy3OYMjXSv87kauGL2wMWbcOulqYRhvoqRwW_OZLqInT-BxOQ_3cjWinuXsFtE3erAqVCIiAq5rpeI0GpBegf9LQlwkC8AwWd39tus86tCjPMpqFSVGDDKzULuw2at72IIavCIO1QrVYpEPeNldTVuapQj4R6LIGz-UrTACM6VMM5XmFmWBWTjI6wwAAAAGKjtBIAQ",
)

OWNER_ID = int(os.getenv("OWNER_ID", "1860375797"))

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

SKY = int(os.getenv("SKY", "-1001933717453"))

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb+srv://aristaa23:1234@cluster0.8yu47ab.mongodb.net/?retryWrites=true&w=majority",
)

DB_URI = os.getenv(
    "DB_URI",
    "postgres://ghomtbxn:mIY6uBsxHsxUsQuOmKkou3ZwAy82aR2i@arjuna.db.elephantsql.com/ghomtbxn",
)
