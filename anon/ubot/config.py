import os

from dotenv import load_dotenv

load_dotenv()


DEVS = [
     2100442624,
]

KYNAN = list(
    map(
        int,
        os.getenv(
            "ANON",
            "2100442624"
        ).split(),
    )
)

API_ID = int(os.getenv("API_ID", "14687692"))

API_HASH = os.getenv("API_HASH", "01581fe794e8242d7da24efd2bea503c")

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1002012397923"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001608847572 -1001538826310 -1001876092598 -1001901142509 -1001974313872 -1001883961446 -1001964273937 -1001986858575 -1001951721136 -1002012397923 -1002045881007 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001861414061 -1001387666944",
        ).split(),
    )
)

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "2100442624",
        ).split(),
    )
)

OPENAI_KEY = os.getenv(
    "OPENAI_KEY", "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"
)

#

BOT_TOKEN = os.getenv("BOT_TOKEN", "6940925615:AAE1SkvF0l_zMUcUZfHN5pU7DYJ7-BCKcrg")

#
#
#

BOT_SESSION = os.getenv(
    "BOT_SESSION",
    "BQAY8JIAwQXpxferOiI7an6Wsy532sLNM6nkhm70q6PNE1hiBEhtrBjP3xr35wvOJwO6PFeBL6anW25_gou1oP6W8hT8jgj-NUUwt2CzlQQWsgsISnGbXSeE_DdmgXuVIHedrbOjh9zxZD1-XtSptTlY8QFgKw4Uy0r2uV1Ycrl1nRnwaq4BCwWg47xuUvtc7NHetxnQC4SzM3J6ca0SG0xHbcpQftNGJz-7JQLfgYBJ-xJxbX728GpG-WnByfAUJrFieOwQc3yCUDt1TPcDzAkoXojocgfDQxcQFWRu-Qe2bUbzBfQ7XkBS5BfbNKL5f28DzSXKOdrlQ6oE3Z0P87xcITARTwAAAAGdth6vAQ",
)

OWNER_ID = int(os.getenv("OWNER_ID", "2100442624"))

MAX_BOT = int(os.getenv("MAX_BOT", "10"))

SKY = int(os.getenv("SKY", "-1001817670395"))

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://argav4:1234@cluster0.ccvngm7.mongodb.net/?retryWrites=true&w=majority",
)

DB_URI = os.getenv(
    "DB_URI",
    "postgres://xsudtorz:C7a4dwxp_mL9He3ffWYvqpGu1R1GuHam@hansken.db.elephantsql.com/xsudtorz"
)
