import sys

from pyrogram import Client
from pyromod import listen
from Amang.config import *

from ..logging import LOGGER


class AmangBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot")
        super().__init__(
            "Amang",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        try:
            await self.send_message(
                LOGS, "Bot Started"
            )
        except:
            pass
        if get_me.last_name:
            self.name = f"{get_me.first_name} {get_me.last_name}"
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"Bot Started as {self.name}")