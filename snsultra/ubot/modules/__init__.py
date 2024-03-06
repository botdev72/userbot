from glob import glob
from os.path import basename, dirname, isfile

from pyrogram import *
from pyrogram.types import *

from ubot import *
from ubot.config import *
from ubot.utils import *

async def cobadah(message):
    user_id = message.from_user.id
    apaan = await get_pref(user_id)
    if apaan == '':
        jadinya = ""
    else:
        jadinya = apaan[0]

BLACKLIST_CHAT = [
    -1001599474353,
    -1001692751821,
    -1001473548283,
    -1001459812644,
    -1001433238829,
    -1001476936696,
    -1001327032795,
    -1001294181499,
    -1001419516987,
    -1001209432070,
    -1001296934585,
    -1001481357570,
    -1001459701099,
    -1001109837870,
    -1001485393652,
    -1001354786862,
    -1001109500936,
    -1001387666944,
    -1001390552926,
    -1001752592753,
    -1001777428244,
    -1001771438298,
    -1001287188817,
    -1001812143750,
    -1001883961446,
    -1001753840975,
    -1001896051491,
    -1001578091827,
    -1001284445583,
    -1001927904459,
    -1001675396283,
    -1001825363971,
    -1001864253073,
    -1001797285258,
    -1001648538608,
    -1001451642443,
    -1001608701614,
]


def loadModule():
    mod_paths = glob(f"{dirname(__file__)}/*.py")
    return sorted(
        [
            basename(f)[:-3]
            for f in mod_paths
            if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
        ]
    )
