from pyrogram import filters

from ubot import anjay, bot, ubot
from ubot.utils.dbfunctions import *


class KY:
    @staticmethod
    def BOT(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def GC():
        def wrapper(func):
            @ubot.on_message(
                filters.group
                & filters.mentioned
                & filters.incoming
                & ~filters.bot
                & ~filters.via_bot
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def PC():
        def wrapper(func):
            @ubot.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.service
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def PM():
        def wrapper(func):
            @ubot.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.via_bot
                & ~filters.service,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def UBOT(command, sudo=False):
        def wrapper(func):
            sudo_command = anjay(command) if sudo else anjay(command) & filters.me

            @ubot.on_message(sudo_command)
            async def wrapped_func(client, message):
                if sudo:
                    sudo_id = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")
                    if client.me.id not in sudo_id:
                        sudo_id.append(client.me.id)
                    if message.from_user.id in sudo_id:
                        return await func(client, message)
                else:
                    return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def INLINE(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
