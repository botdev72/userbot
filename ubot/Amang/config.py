from os import getenv

from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [
    1054295664,
    2073506739,
    1755047203,
    1898065191,
    2133148961,
    1889573907,
    918837361,

]
API_ID = int(getenv("API_ID", "1634450"))


API_HASH = getenv("API_HASH", "1a42e816cae8d86e71a4c466bba19b8c")

BOT_TOKEN = getenv("BOT_TOKEN", "5488425476:AAGh-TSIoPCiGS8AiKB5D6h5ah_VZIjJtUA")

OWNER = int(getenv("OWNER", "2073506739"))


MAX_BOT = int(getenv("MAX_BOT", "30"))

RESI = getenv(
    "RESI", "26646379b9945347b1fc403cb40bcbc6407f1f8106ba8d4b02a9b399999d100c")

LOGS = int(getenv("LOGS", "-1001825904579"))

COMMAND = getenv("COMMAND", ". , ? ;")
cmd = COMMAND.split()

DB_URL = getenv(

    "DATABASE_URL",

    "postgres://mcclbjwx:CqMrbec47cqL5KbaZOUDlVQWOscjNcKR@peanut.db.elephantsql.com/mcclbjwx",
)

BLACKLIST_CHAT = list(
    map(
        int,
        getenv(
            "BLACKLIST_CHAT",
            "-1001692751821 -1001473548283 -1001459812644 -1001433238829 -1001476936696 -1001327032795 -1001294181499 -1001419516987 -1001209432070 -1001296934585 -1001481357570 -1001459701099 -1001109837870 -1001485393652 -1001354786862 -1001109500936 -1001387666944 -1001390552926 -1001752592753 -1001777428244 -1001771438298 -1001287188817 -1001812143750 -1001883961446 -1001753840975 -1001896051491 -1001578091827 -1001927904459"
        ).split(),
    )
)


MONGO_URL = getenv(
    "MONGO_URL",
    "mongodb+srv://VegetaMusic:Vegeta@cluster0.dohyl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
)

SESSION_STRING = getenv(
    "SESSION",
    "",
)

