import os

from dotenv import load_dotenv

load_dotenv()


DEVS = [
    6778133779 # Akiaki
]

KYNAN = list(
    map(
        int,
        os.getenv(
            "KYNAN",
            "6778133779",
        ).split(),
    )
)

API_ID = int(os.getenv("API_ID", "17250424"))

API_HASH = os.getenv("API_HASH", "753bc98074d420ef57ddf7eb1513162b")

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1002110839732"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1002062073372",
        ).split(),
    )
)

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "6778133779",
        ).split(),
    )
)

SUDO_ORANG = list(map(int, os.getenv("SUDO_ORANG", "").split()))

OPENAI_KEY = os.getenv(
    "OPENAI_KEY", "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"
)

#

BOT_TOKEN = os.getenv("BOT_TOKEN", "6199563690:AAHCFS5lXIMnWXBTzWmKz9DQyQGe7poLNbY")

#
#
#

BOT_SESSION = os.getenv(
    "BOT_SESSION",
    "BQEHOHgAItX8wOjrE0Qx05Cqk4biee7YaXyPy3NYhbAs6i7ilo-x57zA9UANWHBv5o8YyglqcoZ5CFNE-cP8bz0DvDStv8beyJJM4G9MUhjpEfgqWKqev79_h_PvawTIvwbT4JWQd28w9PaXIReGkpXQ4TNRAWUvPG3I_tWdKZiiVzQZ0Ggali6ej5wELEugTI5FwGerBSoHYj9q2887LJ7dXYkM1WFzyYj6vBeEOJjbuXXHyzOe6tfq7yC40rurX1tpV_H2I37iLJ6ZEJk-pGIkQfHQNPAmMN9wIEvfWZSpA2HoB2uKM3lB5Rq2nC1jUmndUzy4A4HxwsgwLU05ekx9D9P0fgAAAAFu5ClkAQ",
)

OWNER_ID = int(os.getenv("OWNER_ID", "6778133779"))

MAX_BOT = int(os.getenv("MAX_BOT", "40"))

SKY = int(os.getenv("SKY", "-1002110839732"))

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://zyric:1234@cluster0.bophvmo.mongodb.net/?retryWrites=true&w=majority")

DB_URI = os.getenv(
    "DB_URI",
    "postgres://bikcgkei:pQquEfCrtiNBbRF_WomeGJZNHmqDr7Xo@suleiman.db.elephantsql.com/bikcgkei",
)
