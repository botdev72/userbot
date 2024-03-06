import base64
from base64 import b64decode as kc

import aiohttp
import requests


from pyrogram import *
from pyrogram.types import *

from ubot import *
from ubot.utils import *


@ubot.on_message(anjay("ip") & filters.me)
async def ip_lookup(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Ip address is missing")
    ip_address = message.command[1]
    msg = await message.reply_text("Checking ip address...")
    try:
        res = await http.get(f"https://ipinfo.io/{ip_address}/json", timeout=5)
    except asyncio.TimeoutError:
        return await message.reply_text("request timeout")
    except Exception as e:
        return await message.reply_text(f"ERROR: `{e}`")
    hostname = res.get("hostname", "N/A")
    city = res.get("city", "N/A")
    region = res.get("region", "N/A")
    country = res.get("country", "N/A")
    location = res.get("loc", "N/A")
    org = res.get("org", "N/A")
    await msg.edit(
        (
            f"**Details of `{ip_address}`**\n\n"
            f"HostName: `{hostname}`\n"
            f"City: `{city}`\n"
            f"Region: `{region}`\n"
            f"Country: `{country}`\n"
            f"Org: `{org}`\n"
            f"Map: https://www.google.fr/maps?q={location}\n"
        ),
        disable_web_page_preview=True,
    )


@ubot.on_message(anjay("ipd") & filters.me)
async def whois_domain_target(client, message):
    apikey = base64.b64decode("M0QwN0UyRUFBRjU1OTQwQUY0NDczNEMzRjJBQzdDMUE=").decode(
        "utf-8"
    )
    ran = await message.reply("<code>Processing...</code>")
    domain_text = message.text.split(None, 1)[1] if len(message.command) != 1 else None
    if not domain_text:
        await ran.edit("Example: <code>+ip your ip address here : 1592.401.xxx</code>")
        return

    if not apikey:
        await ran.edit("Missing apikey ip domain")
        return

    url_api_domain = f"https://api.ip2whois.com/v2?key={apikey}&domain={domain_text}"
    whois_domain = ""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_api_domain) as response:
                if response.status == 200:
                    data_domain = await response.json()
                    domain_domain = data_domain.get("domain")
                    domain_domainid = data_domain.get("domain_id")
                    domain_status = data_domain.get("status")
                    domain_create_date = data_domain.get("create_date")
                    domain_update_date = data_domain.get("update_date")
                    domain_expire_date = data_domain.get("expire_date")
                    domain_ages = data_domain.get("domain_age")
                    domain_server = data_domain.get("whois_server")
                    domain_name = data_domain.get("name")
                    domain_organization = data_domain.get("organization")
                    domain_addres = data_domain.get("street_address")
                    domain_city = data_domain.get("city")
                    domain_region = data_domain.get("region")
                    domain_country = data_domain.get("country")
                    domain_email = data_domain.get("email")
                    domain_zip = data_domain.get("zip_code")
                    domain_phone = data_domain.get("phone")
                    domain_nameservers = data_domain.get("nameservers")

                    if (
                        domain_domain
                        and domain_domainid
                        and domain_status
                        and domain_create_date
                        and domain_update_date
                        and domain_expire_date
                        and domain_ages
                        and domain_server
                        and domain_name
                        and domain_organization
                        and domain_addres
                        and domain_city
                        and domain_region
                        and domain_country
                        and domain_email
                        and domain_zip
                        and domain_phone
                        and domain_nameservers
                    ):
                        whois_domain += f"<b>Domain:</b> {domain_domain}\n"
                        whois_domain += f"<b>Domain ID:</b> {domain_domainid}\n"
                        whois_domain += f"<b>Status:</b> {domain_status}\n"
                        whois_domain += f"<b>Create date:</b> {domain_create_date}\n"
                        whois_domain += f"<b>Update date:</b> {domain_update_date}\n"
                        whois_domain += f"<b>Expire date:</b> {domain_expire_date}\n"
                        whois_domain += f"<b>Age:</b> {domain_ages}\n"
                        whois_domain += f"<b>Whois_server:</b> {domain_server}\n"
                        whois_domain += f"<b>Name:</b> {domain_name}\n"
                        whois_domain += f"<b>Organization:</b> {domain_organization}\n"
                        whois_domain += f"<b>Street address:</b> {domain_addres}\n"
                        whois_domain += f"<b>City:</b> {domain_city}\n"
                        whois_domain += f"<b>Region:</b> {domain_region}\n"
                        await ran.edit(whois_domain)
                    else:
                        await ran.edit("No data for this domain.")
                else:
                    await ran.edit("Error: could not fetch WHOIS information.")
    except Exception as e:
        await ran.edit(f"Error: {str(e)}")


__MODULE__ = "IpSearch"
__HELP__ = """
Bantuan Untuk IP Search


• Perintah: <code>{0}ip</code> [ip host]
• Penjelasan: Untuk mencari lokasi ip addres.

• Perintah: <code>{0}ipd</code> [ip domain]
• Penjelasan: Untuk mencari lokasi ip domain.
"""
