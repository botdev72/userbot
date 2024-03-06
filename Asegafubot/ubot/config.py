import os

from dotenv import load_dotenv

load_dotenv()


DEVS = [
    1054295664,
    1889281820,
    1609735679,
    482945686,
    6389355751,
    816526222,  # Lucifer
]

KYNAN = list(map(int, os.getenv("KYNAN", "1054295664 1889281820 1609735679 482945686 6389355751 816526222").split()))

API_ID = int(os.getenv("API_ID", "17250424"))

API_HASH = os.getenv("API_HASH", "753bc98074d420ef57ddf7eb1513162b")

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1001778769772"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001608847572 -1001538826310 -1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001861414061 -1001387666944 -1001986858575",
        ).split(),
    )
)

USER_ID = list(map(int, os.getenv("USER_ID", "1889281820 1609735679 6389355751 6619580284 482945686").split()))

OPENAI_KEY = os.getenv(
    "OPENAI_KEY", "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"
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "6495318627:AAHSRLsCqo2KW-P_mb573KAIQF4_mqD91Aw")


BOT_SESSION = os.getenv(
    "BOT_SESSION",
    "BQAY8JIAQw7GJPqJUvms7irpPsJrx06WivBVk_Z19iM5CBBCXY0fW_zYSWXrRgm6GF6kcgfXVUv-qzPT3qiD7goaFAxIPYur3NRh7x1XJOHOnedFbluKbPe_oPCGHG-TYyC3KquRb76RCJ_Ko9jekHIyfcy8yKOULtaJjBWG3opC_G-A_fj-SHh8-HinLkwlTRZ7eUiVPWj2JH00d8mvZRmCAFQs5uGlfn_W7xlAZLx-dAsNnWMuZ9VECccJQNdpnxEiwMwg_yxk-p2-iMjvsBMZie8CBoh_Q2JhqEGf_5ooYKzR25j5idj7KeO2fVczeJAYbvGI7obvFINEB7jcCR0FasxhLgAAAAGDJrJjAQ",
)

OWNER_ID = int(os.getenv("OWNER_ID", "6619580284"))

MAX_BOT = int(os.getenv("MAX_BOT", "25"))

SKY = int(os.getenv("SKY", "-1002116277342"))


MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://alcan03:4444@cluster0.nlenldp.mongodb.net/?retryWrites=true&w=majority",
)

DB_URI = os.getenv(
    "DB_URI",
    "postgres://mcclbjwx:CqMrbec47cqL5KbaZOUDlVQWOscjNcKR@peanut.db.elephantsql.com/mcclbjwx",
)
