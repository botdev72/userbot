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
    920149276, #Mikientod
    955046926, #uput3
    1996712837, #aul
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
            "-1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001608847572 -1001982790377 -1001538826310 -1001861414061 -1001876092598 -1001986858575 -1002086224621",
        ).split(),
    )
)

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "482945686 1860375797 712277262 816526222 479344690 920149276",
        ).split(),
    )
)

OPENAI_KEY = os.getenv(
    "OPENAI_KEY", "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"
)


BOT_TOKEN = os.getenv(
    "BOT_TOKEN", "6466675652:AAEjoUimSMjaU-bnvMHZd8iAmS2sQ8D68bM"
)

BOT_SESSION = os.getenv(
    "BOT_SESSION",
    "BQFi8RAAbUcu5h_UG1aBs0TzGPdfFLSMMG1O8fNB_bEB-Lt7JhR201mCYkOJqDlvwh0xzgeIdkQOjiPvJNgRkdWYFdHxLWacqYqPBMB2wTrb1seABRPRxOTJO3ZNs2AA1QDEmQGtI2W2ZuEAMLUqJxBnyo9CE-YYoe_CJF_hl6SjutrGAFyysMd4aY-PRA8IJwfKXg1i6IdXZJ0yZju7BPRTHVrYGXiKAulCERm0iJF58LQRp5epT2UqyEJeAd1UeGreXKQLbzAN3lRyLHdAtPBRf1yPAglVxgIObXuDue72gLNYmgC71K2UK6iTHoKYZ9O_36Etbe633iVG7zEzPCcsc6sUUwAAAAGBcaPEAQ",
)

OWNER_ID = int(os.getenv("OWNER_ID", "1860375797"))

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

SKY = int(os.getenv("SKY", "-1001933717453"))

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb+srv://sky:sky@cluster0.g9rvgeu.mongodb.net/?retryWrites=true&w=majority",
)

DB_URI = os.getenv(
    "DB_URI",
    "postgres://dyvaogqu:AAZJNH09blvxIVOj9t6CGQssvMp3lNvl@rain.db.elephantsql.com/dyvaogqu",
)
