import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "1634450"))


API_HASH = os.environ.get("API_HASH", "1a42e816cae8d86e71a4c466bba19b8c")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6047134953:AAGl1pf44VOe7ACMfTah8YPtbDayO9rEPPs")

OWNER = int(os.environ.get("OWNER", "1839010591"))

OPENAI_API = os.environ.get("OPENAI_API", "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")

MAX_UBOT = int(os.environ.get("MAX_BOT", "20"))

SELLER_GROUP= int(os.environ.get("SELLER_GROUP", "-1001655255241"))

RESI = os.environ.get(
    "RESI", "26646379b9945347b1fc403cb40bcbc6407f1f8106ba8d4b02a9b399999d100c")

LOGS = int(os.environ.get("LOGS", "-1001753711304"))

COMMAND = os.environ.get("COMMAND", ". , - ! ?")
cmd = COMMAND.split()

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001692751821 -1001473548283 -1001459812644 -1001433238829 -1001476936696 -1001327032795 -1001294181499 -1001419516987 -1001209432070 -1001296934585 -1001481357570 -1001459701099 -1001109837870 -1001485393652 -1001354786862 -1001109500936 -1001387666944 -1001390552926 -1001752592753 -1001777428244 -1001771438298 -1001287188817 -1001812143750 -1001883961446 -1001753840975 -1001896051491 -1001578091827 -1001927904459 -1001578854150 -1001953239597 -1001704645461"
        ).split(),
    )
)


MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://VegetaMusic:Vegeta@cluster0.dohyl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
if MONGO_URL:
    MONGO_URL = MONGO_URL.split()

SESSION = os.environ.get(
    "SESSION",
    "",
)
