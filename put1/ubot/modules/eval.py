import sys
import traceback
from io import BytesIO, StringIO
import asyncio
import os
import subprocess
import platform
import traceback
from datetime import datetime
import time
import psutil
from os import execvp
from sys import executable
from subprocess import Popen, PIPE, TimeoutExpired
from time import perf_counter

from ubot import *
from ubot.utils import *


async def restart():
    execvp(executable, [executable, "-m", "ubot"])


@bot.on_message(filters.command("update") & filters.user(USER_ID))
@ubot.on_message(anjay("update|up") & filters.user(USER_ID) & filters.me)
async def update_restart(_, message):
    xx = await message.reply("Processing...")
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            return await xx.edit("Its already up-to date!")
        await xx.edit(f"```{out}```")
    except Exception as e:
        return await xx.edit(str(e))
    await xx.delete()
    await message.delete()
    await restart()
    

@bot.on_message(filters.command(["sh"]) & filters.user(USER_ID))
@ubot.on_message(anjay("sh") & filters.user(USER_ID) & filters.me)
async def shell(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("<b>Specify the command in message text</b>")
    cmd_text = message.text.split(maxsplit=1)[1]
    cmd_obj = Popen(
        cmd_text,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )

    char = "#" if os.getuid() == 0 else "$"
    text = f"<b>{char}</b> <code>{cmd_text}</code>\n\n"

    mmk = await message.reply(text + "<b>Running...</b>")
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            text += f"<b>Output:</b>\n<code>{stdout}</code>\n\n"
        if stderr:
            text += f"<b>Error:</b>\n<code>{stderr}</code>\n\n"
        text += f"<b>Completed in {round(stop_time - start_time, 5)} seconds with code {cmd_obj.returncode}</b>"
        if int(len(str(text))) > 4096:
            with BytesIO(str.encode(str(text))) as out_file:
                out_file.name = "result.txt"
                await message.reply_document(
                    document=out_file,
                )
                await mmk.delete()
        else:
            await mmk.edit(text)
    cmd_obj.kill()


@ubot.on_message(anjay("trash") & filters.user(USER_ID) & filters.me)
async def _(client, message):
    msgs = message.reply_to_message
    if message.reply_to_message:
        try:
            if len(message.command) < 2:
                if len(str(message.reply_to_message)) > 4096:
                    with BytesIO(str.encode(str(message.reply_to_message))) as out_file:
                        out_file.name = "trash.txt"
                        return await message.reply_document(document=out_file)
                else:
                    return await message.reply(msgs)
            else:
                value = eval(f"message.reply_to_message.{message.command[1]}")
                return await message.reply(value)
        except Exception as error:
            return await message.reply(str(error))
    else:
        return await message.reply("bukan gitu caranya")



@ubot.on_message(anjay("eval") & filters.user(USER_ID) & filters.me)
@bot.on_message(filters.command(["eval"]) & filters.user(USER_ID))
async def _(client, message):
    cmd = message.text.split(" ", maxsplit=1)[1]
    if not cmd:
        return await message.reply("`Give me commands dude...`")
    else:
        ajg = await message.reply("`Processing ...`")
    reply_to_ = message.reply_to_message or message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "OUTPUT:\n"
    final_output += f"{evaluation.strip()}"
    if len(final_output) > 4096:
        with BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd[: 4096 // 4 - 1],
                disable_notification=True,
                quote=True,
            )
    else:
        await reply_to_.reply_text(final_output, quote=True)
    await ajg.delete()


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@ubot.on_message(anjay("host") & filters.user(USER_ID) & filters.me)
async def cek_host(client, message):
    xx = await message.reply("Processing...")
    uname = platform.uname()
    softw = "Informasi Sistem\n"
    softw += f"Sistem   : {uname.system}\n"
    softw += f"Rilis    : {uname.release}\n"
    softw += f"Versi    : {uname.version}\n"
    softw += f"Mesin    : {uname.machine}\n"

    boot_time_timestamp = psutil.boot_time()

    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}\n"

    softw += "\nInformasi CPU\n"
    softw += "Physical cores   : " + str(psutil.cpu_count(logical=False)) + "\n"
    softw += "Total cores      : " + str(psutil.cpu_count(logical=True)) + "\n"
    cpufreq = psutil.cpu_freq()
    softw += f"Max Frequency    : {cpufreq.max:.2f}Mhz\n"
    softw += f"Min Frequency    : {cpufreq.min:.2f}Mhz\n"
    softw += f"Current Frequency: {cpufreq.current:.2f}Mhz\n\n"
    softw += "CPU Usage Per Core\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        softw += f"Core {i}  : {percentage}%\n"
    softw += "Total CPU Usage\n"
    softw += f"Semua Core: {psutil.cpu_percent()}%\n"

    softw += "\nBandwith Digunakan\n"
    softw += f"Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}\n"
    softw += f"Download: {get_size(psutil.net_io_counters().bytes_recv)}\n"

    svmem = psutil.virtual_memory()
    softw += "\nMemori Digunakan\n"
    softw += f"Total     : {get_size(svmem.total)}\n"
    softw += f"Available : {get_size(svmem.available)}\n"
    softw += f"Used      : {get_size(svmem.used)}\n"
    softw += f"Percentage: {svmem.percent}%\n"

    await xx.edit(f"<b>{softw}</b>")


@ubot.on_message(anjay("user") & filters.user(USER_ID) & filters.me)
async def liat_berapa(client, message):
    tt = await message.reply("**Bentar diliat...**")
    xx = len(ubot._ubot)
    await tt.edit(f"**Jumlah induk baruak : `{xx}`**")
