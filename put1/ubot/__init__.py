import logging
import re
import time
from os import execvp
from sys import executable

from aiohttp import ClientSession
from pyrogram import *
from pyrogram.handlers import *
from pyrogram.types import *
from pyromod import listen
import pytgcalls

from ubot.config import *

aiosession = ClientSession()

CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
PLAYOUT_FILE = "/ubot/resources/vc.mp3"
OUTGOING_AUDIO_BITRATE_KBIT = 218

class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for X in ["OSErro", "OSError", "socket"]:
            if X in record.getMessage():
                execvp(executable, [executable, "-m", "ubot"])


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)

LOGS = logging.getLogger(__name__)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []
    _prefix = {}
    #_get_my_id = []
    #_translate = {}
    #_get_my_peer = {}

    def __init__(self, api_id, api_hash, device_model="v1uputt", **kwargs):
        super().__init__(**kwargs)
        self.api_id = api_id
        self.api_hash = api_hash
        self.device_model = device_model
        self.vc = pytgcalls.GroupCallFactory(
            self, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
        ).get_file_group_call(PLAYOUT_FILE)

    def on_message(self, filters=None, group=0):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def set_prefix(self, user_id, prefix):
        self._prefix[self.me.id] = prefix

    async def start(self):
        await super().start()
        handler = await get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._ubot.append(self)
        #self._get_my_id.append(self.me.id)
        #self._translate[self.me.id] = {"negara": "id"}
        print(f"Starting Userbot ({self.me.id}|{self.me.first_name})")


ubot = Ubot(
    name="ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="v4uputt",
)


async def get_prefix(user_id):
    return ubot._prefix.get(user_id, [".", "?", "!"])


def anjay(cmd):
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(_, client, message):
        if message.text:
            text = message.text.strip().encode("utf-8").decode("utf-8")
            username = client.me.username or ""
            prefixes = await get_prefix(client.me.id)

            if not text:
                return False

            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix) :]

                for command in cmd.split("|"):
                    if not re.match(
                        rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                        without_prefix,
                        flags=re.IGNORECASE | re.UNICODE,
                    ):
                        continue

                    without_command = re.sub(
                        rf"{command}(?:@?{username})?\s?",
                        "",
                        without_prefix,
                        count=1,
                        flags=re.IGNORECASE | re.UNICODE,
                    )
                    message.command = [command] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True

        return False

    return filters.create(func)


class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_message(self, filters=None, group=0):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=0):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()


bot = Bot(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    #session_string=BOT_SESSION,
    device_model="v1uputt",
)

from ubot.core.helpers import *
from ubot.utils.dbfunctions import *
