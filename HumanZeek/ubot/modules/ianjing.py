import traceback


from ubot.core.functions.plugins import HELP_COMMANDS
from ubot.utils.misc import paginate_modules
from pyrogram.raw.functions import Ping
from pyrogram.types import *
from pyrogram import *

from ubot import *
from ubot.utils import *
from ubot.config import *

"""
#@bot.on_inline_query(filters.regex("monyet"))
async def si_monyed(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.strip() == "help":
            answerss = await help_anjing(query)
            return await client.answer_inline_query(
                query.id, results=answerss, cache_time=0
            )
    except Exception as e:
        e = traceback.format_exc()
        print(e, " InLine")


async def help_anjing(query):
    answers = []
    user_id = query.from_user.id
    emut = await get_pref(user_id)
    if emut is not None:
        msg = "<b>Help Modules\n     Prefixes: <code>{}</code>\n     Commands: <code>{}</code></b>".format(emut[0], len(HELP_COMMANDS))
    elif emut == [""]:
        msg = "<b>Help Modules\n     Prefixes: `None`\n     Commands: <code>{}</code></b>".format(len(HELP_COMMANDS))
    else:
        msg = "<b>Help Modules\n     Prefixes: `None`\n     Commands: <code>{}</code></b>".format(len(HELP_COMMANDS))
    answers.append(
        InlineQueryResultArticle(
            title="Help",
            input_message_content=InputTextMessageContent(msg),
            reply_markup=InlineKeyboardMarkup(paginate_modules(0,
            HELP_COMMANDS, "help")),
        )
    )
    return answers
"""