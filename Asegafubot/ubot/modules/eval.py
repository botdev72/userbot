import asyncio
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from os import execvp
from subprocess import PIPE, Popen, TimeoutExpired
from sys import executable
from time import perf_counter

import psutil
from psutil._common import bytes2human

from ubot import *
from ubot.utils import *

from .gcast import get_message


async def restart():
    execvp(executable, [executable, "-m", "ubot"])


@KY.BOT("update", FIL.SUDO)
@KY.UBOT("update|up", FIL.ME_USER)
async def update_restart(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(0.5)
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


@KY.BOT("sh", FIL.SUDO)
@KY.UBOT("sh", FIL.ME_USER)
async def shell(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
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

    mmk = await message.reply(text + f"{emo.proses} <b>Running...</b>")
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += f"{emo.gagal} <b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            text += f"{emo.sukses} <b>Output:</b>\n<code>{stdout}</code>\n\n"
        if stderr:
            text += f"{emo.gagal} <b>Error:</b>\n<code>{stderr}</code>\n\n"
        text += f"{emo.sukses} <b>Completed in {round(stop_time - start_time, 5)} seconds with code {cmd_obj.returncode}</b>"
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


@KY.UBOT("trash", FIL.ME_USER)
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


@KY.BOT("eval", FIL.SUDO)
@KY.UBOT("eval|ev", FIL.ME_USER)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    reply_to_ = get_message(message)
    cmd = message.text.split(" ", maxsplit=1)[1]
    xx = await message.reply(f"{emo.proses} **Processing ...**")
    if not (reply_to_, cmd):
        await xx.edit(f"{emo.proses} **Give text or reply...**")
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
        evaluation = f"**Success**"
    final_output = f"{emo.sukses} **OUTPUT:**\n"
    final_output += f"{emo.sukses} **{evaluation.strip()}**"
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
        await xx.edit(final_output)
    # await ajg.delete()


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@KY.BOT("host", FIL.SUDO)
@KY.UBOT("host", FIL.ME_USER)
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


@KY.UBOT("user", FIL.ME_USER)
async def liat_berapa(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = len(ubot._ubot)
    tt = await message.reply(f"**{emo.proses} Procesing...**")
    await asyncio.sleep(0.5)
    await tt.edit(f"**{emo.sukses} Jumlah Babi Liar Ada : `{xx}`**")


async def generate_sysinfo(workdir):
    # user total

    # uptime
    info = {
        "BOOT": (
            datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        )
    }
    # CPU
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    info["CPU"] = (
        f"{psutil.cpu_percent(interval=1)}% " f"({psutil.cpu_count()}) " f"{cpu_freq}"
    )
    # Memory
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    info["RAM"] = f"{bytes2human(vm.used)}, " f"/ {bytes2human(vm.total)}"
    info["SWAP"] = f"{bytes2human(sm.total)}, {sm.percent}%"
    # Disks
    du = psutil.disk_usage(workdir)
    dio = psutil.disk_io_counters()
    info["DISK"] = (
        f"{bytes2human(du.used)} / {bytes2human(du.total)} " f"({du.percent}%)"
    )
    if dio:
        info[
            "DISK I/O"
        ] = f"R {bytes2human(dio.read_bytes)} | W {bytes2human(dio.write_bytes)}"
    # Network
    nio = psutil.net_io_counters()
    info[
        "NET I/O"
    ] = f"TX {bytes2human(nio.bytes_sent)} | RX {bytes2human(nio.bytes_recv)}"
    # Sensors
    sensors_temperatures = psutil.sensors_temperatures()
    if sensors_temperatures:
        temperatures_list = [x.current for x in sensors_temperatures["coretemp"]]
        temperatures = sum(temperatures_list) / len(temperatures_list)
        info["TEMP"] = f"{temperatures}\u00b0C"
    info = {f"{key}:": value for (key, value) in info.items()}
    max_len = max(len(x) for x in info)
    return (
        "<code>\n"
        + "\n".join([f"{x:<{max_len}} {y}" for x, y in info.items()])
        + "</code>"
    )


@KY.UBOT("stats", FIL.ME_USER)
async def stats_vps(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    response = await generate_sysinfo(client.workdir)
    anu = await get_userbots()
    await message.reply(
        f"{emo.proses} <b># {bot.me.first_name}</b>\n<code>stats : total {len(anu)} users jembut</code>\n"
        + response
    )


@KY.UBOT("upgrade", FIL.SUDO)
@KY.UBOT("update|up", FIL.ME_USER)
async def the_reboot(client, message):
    await message.delete()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, "-m", "ubot")