import os

from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [
    1557184285, #Kage
    1955038230
]


API_ID = int(os.environ.get("API_ID", "22576593"))


API_HASH = os.environ.get("API_HASH", "58dc5b6dc6b5408ff95dadb84ba148f4")


OPENAI_API = os.environ.get("OPENAI_API", "ssk-f3185kP8hFfcOeONlTRrT3BlbkFJjwAMOE92hL7OdpgBwuyR")


BOT_TOKEN = os.environ.get("BOT_TOKEN", "6492767548:AAEfuRARMAjqpOjsHbsx0Cqg5JsG-B-arws")


OWNER_ID = int(os.environ.get("OWNER_ID", "1955038230"))


MAX_BOT = int(os.environ.get("MAX_BOT", "50"))


SKY = int(os.environ.get("SKY", "-1001900725213"))


MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb+srv://joshuamusic:joshuamusic@cluster0.0gaxqnn.mongodb.net/?retryWrites=true&w=majority",
)

SESSION_STRING = os.environ.get(
    "SESSION_STRING",
    "BQFfR_YAbwMLAZf5We-EBzRs2KvmbudpPPALpIehU6IGIzBDMMIYxcDqVgQz-Uq54-speQyJG-9Xkk-Uw2hcekEKy0HnX7fWejXtdHnjgr2ydBAHUxtNtM5wgd4tDsiVX884RGzAytuq01LFeBIanylF7tMeGtAB5RfB88Ga5wWa4zUlvUJq2Om29LT5U66GiyksYMP_A3iNB2NXLRKyA5d7PdKuanIMddDOW8I14sjg4hubTtMAi1vkrJ8jZ5EdIfE3M_4svRmm9MpLEPnUUE5MjvWVDjw6veJAwvW9BpwMQqJf_O6yOQW-k30QnV4P-1EgYptKIcjnje9TS8lM1lUhWIpumQAAAAB0h4QWAA",
)
