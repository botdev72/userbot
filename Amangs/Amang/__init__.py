import asyncio
import re
import os
import sys
import time
from os import environ, execle
from datetime import datetime
from pyrogram import *


from aiohttp import ClientSession
from .config import *
from .logging import LOGGER
from pyromod import listen
from pyrogram import *
from pyrogram.handlers import *
from pyrogram.types import *

from Amang.utils.dbfunctions import get_pref
import pytgcalls

StartTime = time.time()

START_TIME = datetime.now()

aiosession = ClientSession()


CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
PLAYOUT_FILE = "/Amang/resources/vc.mp3"
OUTGOING_AUDIO_BITRATE_KBIT = 218


AMANG = [
    2073506739,
    918837361,
    1839010591,
]

DEVS = [
    1054295664,
    2073506739,
    1694909518,
    1898065191,
    918837361,
    1839010591,
]

class Ubot(Client):
    _ubot = []
    _prefix = {}
    _get_my_id = []
    _translate = {}
    _get_my_peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device_model = "AmangBot"
        self.vc = pytgcalls.GroupCallFactory(
            self, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
        ).get_file_group_call(PLAYOUT_FILE)
          
    def on_message(self, filters=None, group=-1):
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
        self._prefix[self.me.id] = handler if handler else [".", "!"]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = {"negara": "id"}
        print(f"[𝐈𝐍𝐅𝐎] - ({self.me.id}) - 𝐒𝐓𝐀𝐑𝐓𝐄𝐃")


async def get_prefix(user_id):
    return ubot._prefix.get(user_id, ".")


def anjay(cmd):
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
 
    async def func(_, client, message):
        if message.text and message.from_user:
            text = message.text.strip()
            username = client.me.username or ""
            prefixes = await get_prefix(client.me.id)

            if not text:
                return False

            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix) :]

                for command in [cmd]:
                    if not re.match(
                        rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                        without_prefix,
                        flags=re.IGNORECASE if not False else 0,
                    ):
                        continue

                    without_command = re.sub(
                        rf"{command}(?:@?{username})?\s?",
                        "",
                        without_prefix,
                        count=1,
                        flags=re.IGNORECASE if not False else 0,
                    )
                    message.command = [command] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True

        return False

    return filters.create(func)

ubot = Ubot(name="ubot")

class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="AmangBot", system_version="Windows")

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
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
)
