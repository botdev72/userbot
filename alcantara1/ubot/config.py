import os

from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [
    1087819304, #reza
    1609735679, #al
    1889281820, #alcantara
    6619580284, #asegaf
    1953140533, #alcan
]


API_ID = int(os.environ.get("API_ID", "23855532"))


API_HASH = os.environ.get("API_HASH", "3cc6eac0a9fbfe0b2b1da77f043cc9c9")


OPENAI_API = os.environ.get("OPENAI_API", "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")


BOT_TOKEN = os.environ.get("BOT_TOKEN", "6431816453:AAHyXRXWS2CRQLPdupcE7xG2RnGDKiiMcjc")


OWNER_ID = int(os.environ.get("OWNER_ID", "6619580284"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1001608847572 -1001538826310 -1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001861414061
  -1001986858575 -1001778769772").split()))

MAX_BOT = int(os.environ.get("MAX_BOT", "40"))


SKY = int(os.environ.get("MLMD", "-1002122882970"))


MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb+srv://mlmdproject:4444@cluster0.czd68hg.mongodb.net/?retryWrites=true&w=majority",
)

SESSION_STRING = os.environ.get(
    "SESSION_STRING",
    "BQAY8JIArP2iWLgOTmqMnC8cqU67pDxqvtF8F2GJLBeVj9Bn7Kz997OFBZOINKDt4b7szCijUIcap9srFsAf6XTKHIGvfe_BlzXMlb705FA5RixHR54vTw0TpTl0xmgmyNKPWM_9xfLpVk0J2wvD0tFDt55akE7iZy95P1AyiJER884R582hcLxOC11tUk3nq6qNsQ9q7onU6w7h7R7E7fU-mIVHebkEYBnDBUXOGjqQykI_9YK70hPItwy8GwU7CxtiCvxTiaPYGP92mjMQ7jkIbOIALOguZpZLqoXwIUs-5XJfxWQppSYYpB3-A-3bY6QcWE6fA2Ej32rBX1XpdmF-pTRbsQAAAAF5oQ0gAA",
)
