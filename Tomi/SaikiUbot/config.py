import os

API_ID = int(os.getenv("API_ID", "2237557"))

API_HASH = os.getenv("API_HASH", "5dcc2172391406707828d375603cc001")

BOT_TOKEN = os.getenv("BOT_TOKEN", "5812805818:AAFkIyT23Y85kLv2kz2ciz2diDXe17o8ZMQ")

OWNER_ID = int(os.getenv("OWNER_ID", "5876222922"))

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1001835199524"))

COMMAND = os.getenv("COMMAND", ". , : ; !⁣")
PREFIX = COMMAND.split()

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1001880331689").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "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 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",
).split()


MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://apn00:apn00@cluster0.r1xeekc.mongodb.net/?retryWrites=true&w=majority",
)

SESSION_STRING = os.getenv(
    "SESSION_STRING",
    "BQAiJHUAhGT-3CRoZCURTSdZ0RtrBVC9CSAoCfPC9UwhaYFy8IAhW1cd9kAV4WwS_sUIGa8meEwRNLe0g1Of5frcWpYFZZHnOSqFKUbKj54XHOR3seFx20KtMKc9jnFjs64e0tBlcaWSsLxExCbaFav4nqaft-Qp3eaR7bpAKYUic2NdfMjDKfZZKfMuQ7msi0K2ucDDxA6oVZloUpLB_2NXg94TrKzLMRrdS-H7BNmhCqFxquGAxE8hx5wLtgPuAq3YHyHHF9_ddZ59Ht1OAMM3Jda_nSjWetR5Poxpk3xGWQSVkQgTC0liTT7gFlgxXtWKdVujCp5Sw_yquvL-pbBoVXpuRAAAAAFeQAvKAA",
)

TEXT_PAYMENT = os.getenv(
    "TEXT_PAYMENT",
    """
<b>💬 SILAHKAN MELAKUKAN PEMBAYARAN SEBESAR RP25.000 = 1 BULAN</b>

<b>💳 MOTODE PEMBAYARAN:</b>
  <b>┣ DANA/GOPAY/OVO/SPAY</b>
  <b>┣    ┗</b> <code>089525658633</code>
  <b>┣ QRIS</b>
  <b>┗    ┗</b> <a href=https://telegra.ph/file/21e888e1960b1ce9392a7.jpg>KLIK DISINI</a>

<b>✅ KLIK TOMBOL KONFIRMASI UNTUK KIRIM BUKTI PEMBAYARAN ANDA</b>
""",
)
