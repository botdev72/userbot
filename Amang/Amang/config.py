from os import getenv
from base64 import b64decode
import base64
from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [
    1839010591,

]
API_ID = int(getenv("API_ID", "1634450"))


API_HASH = getenv("API_HASH", "1a42e816cae8d86e71a4c466bba19b8c")

BOT_TOKEN = getenv("BOT_TOKEN", "6047134953:AAGl1pf44VOe7ACMfTah8YPtbDayO9rEPPs")
OWNER = int(getenv(
    "OWNER",
    b64decode("MTgzOTAxMDU5MQ==").decode(
        "utf-8"
    ),
)
           )

MAX_BOT = int(getenv("MAX_BOT", "20"))

SELLER_GROUP=int(getenv("SELLER_GROUP", "-1001655255241"))

RESI = getenv(
    "RESI", "26646379b9945347b1fc403cb40bcbc6407f1f8106ba8d4b02a9b399999d100c")

LOGS = int(getenv("LOGS", "-1001655255241"))

COMMAND = getenv("COMMAND", ". , ? ;")
cmd = COMMAND.split()

blacklist_chat_encoded = "LTEwMDE2OTI3NTE4MjEgLTEwMDE0NzM1NDgyODMgLTEwMDE0NTk4MTI2NDQgLTEwMDE0MzMyMzg4MjkgLTEwMDE0NzY5MzY2OTYgLTEwMDEzMjcwMzI5NSAtMTAwMTI5NDE4MTQ5OSAtMTAwMTQxOTUxNjk4NyAtMTAwMTIwOTQzMjA3MCAtMTAwMTI5NjkzNDU4NSAtMTAwMTQ4MTM1NzU3MCAtMTAwMTQ1OTcwMTA5OSAtMTAwMTEwOTgzNzg3MCAtMTAwMTQ4NTM5MzY1MiAtMTAwMTM1NDc4Njg2MiAtMTAwMTEwOTUwMDkzNiAtMTAwMTM4NzY2Njk0NCAtMTAwMTM5MDU1MjkyNiAtMTAwMTc1MjU5Mjc1MyAtMTAwMTc3NzQyODI0NCAtMTAwMTc3MTQzODI5OCAtMTAwMTI4NzE4ODgxNyAtMTAwMTgxMjE0Mzc1MCAtMTAwMTg4Mzk2MTQ0NiAtMTAwMTc1Mzg0MDk3NSAtMTAwMTg5NjA1MTQ5MSAtMTAwMTU3ODA5MTgyNyAtMTAwMTkyNzkwNDQ1OSAtMTAwMTU3ODg1NDE1MA=="
decoded_blacklist_chat = base64.b64decode(blacklist_chat_encoded).decode("utf-8")
blacklist_chat_list = decoded_blacklist_chat.split()
blacklist_chat_integers = list(map(int, blacklist_chat_list))
BLACKLIST_CHAT = blacklist_chat_integers


MONGO_URL = getenv(
    "MONGO_URL",
    "mongodb+srv://magicm:magicm@cluster0.8rqp3hg.mongodb.net/?retryWrites=true&w=majority",
)

SESSION = getenv(
    "SESSION",
    "BQEHOHgAURd7SyJs9NQWRzs2U_DOdlD1JL7HkFopnjsPhgAX5ySYSSTpuDR9X_c5BWTSBchlH4PlLjy_GRllePvwjW-GT9ZmsI6N7SO9DK6wD_DSsJAsAg-d8aXOOJkKxrqATUGSxgds3xcrpfU8CDTnRhwaBMlVJ-Q5j_XqOicBj8sMGOsFX8-bVDnmnJZMBhj6H4R1TJ10PKWHsOZOQXn_nn4CmZIiZm7HQtIsJp9-sJp-cLDNprbarsw3u3az6ISL4fG-3jzrKRi1ftZWnYV6JtpsBw9cK4oVw0DtDdjsGP1QVrzFf8KVIoIeGWvsMx8WYuh68R4sHuFQ_TBZFw2D4PX7hAAAAAF_PaDVAA",
)

TEXT_PAYMENT = getenv(
    "TEXT_PAYMENT",
    """
<b>💬 SILAHKAN MELAKUKAN PEMBAYARAN SEBESAR RP25.000 = 1 BULAN</b>

<b> METODE PEMBAYARAN:</b>
   <b>┣ DANA/GOPAY/OVO VIA QRIS</b>
   <b>┗   </b> <a href=https://t.me/amwang/4>KLIK DISINI</a>

<b>✅ KLIK TOMBOL KONFIRMASI UNTUK KIRIM BUKTI PEMBAYARAN ANDA</b>
""",
)
