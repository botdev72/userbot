import logging

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyromod import listen

from .config import *

logging.basicConfig(
    level=logging.ERROR,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[logging.StreamHandler()],
)

bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_message(self, filters: filters.Filter, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        if self not in self._ubot:
            self._ubot.append(self)


ubot = Ubot(
    name="ubot",
    api_id=2237557,
    api_hash="5dcc2172391406707828d375603cc001",
    session_string=SESSION_STRING,
)

get_my_id = []
get_my_peer = {}
lang_code = {}

from .core import *
from .utils import *
