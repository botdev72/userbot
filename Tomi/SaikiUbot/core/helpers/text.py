from SaikiUbot.config import PREFIX

help_admin = [
    f"""
<b>HELP ADMIN GLOBAL

Perintah:
         <code>{PREFIX[0]}gban</code> [user_id/username/reply to user]
Penjelasan:
           Untuk banned user dari semua group chat 

Perintah:
         <code>{PREFIX[0]}ungban</code> [user_id/username/reply to user]
Penjelasan:
           Untuk unbanned user dari semua group chat</b>
""",
    f"""
<b>HELP ADMIN RESTRICT

Perintah:
         <code>{PREFIX[0]}kick</code> [user_id/username/reply user]
Penjelasan:
           Untuk menendang anggota dari grup 

Perintah:
         <code>{PREFIX[0]}ban</code> [user_id/username/reply user]
Penjelasan:
           Untuk memblokir anggota dari grup 

Perintah:
         <code>{PREFIX[0]}mute</code> [user_id/username/reply user]
Penjelasan:
           Untuk membisukan anggota dari grup 

Perintah:
         <code>{PREFIX[0]}unban</code> [user_id/username/reply user]
Penjelasan:
           Untuk melepas pemblokiran anggota dari grup 

Perintah:
         <code>{PREFIX[0]}unmute</code> [user_id/username/reply user]
Penjelasan:
           Untuk melepas pembisuan anggota dari grup</b>
""",
]

help_sticker = [
    f"""
<b>HELP STICKER KANG

Perintah:
         <code>{PREFIX[0]}kang</code> [reply to image/sticker]
Penjelasan:
           Balas Ke Sticker Atau Gambar Untuk Menambahkan Ke Sticker Pack.
           Untuk Menambahkan dan costum emoji sticker Ke Sticker Pack Mu,
           <b>NOTE:</b> Untuk Membuat Sticker Pack baru Gunakan angka dibelakang <code>{PREFIX[0]}kang</code>,
           <b>CONTOH:</b> <code>{PREFIX[0]}kang</code> 2</code> untuk membuat dan menyimpan ke sticker pack ke 2</b>
""",
    f"""
<b>HELP STICKER MEMIFY 

Perintah:
         <code>{PREFIX[0]}mmf</code> [text]
Penjelasan:
           Balas Ke Sticker atau Foto akan Di ubah menjadi sticker teks meme yang di tentukan.</b>
""",
    f"""
<b>HELP STICKER MEMES 

Perintah:
         <code>{PREFIX[0]}memes</code> [text]
Penjelasan:
           Untuk membuat stiker memes random</b>
""",
    f"""
<b>HELP STICKER QUOTLY 

Perintah:
         <code>{PREFIX[0]}q</code> [text/reply to text/media]
Penjelasan:
           Untuk merubah text menjadi sticker</b>
""",
    f"""
<b>HELP STICKER TINY 

Perintah:
         <code>{PREFIX[0]}tiny</code> [reply to sticker]
Penjelasan:
           Untuk merubah sticker menjadi kecil</b>
""",
]

HelpText = {
    "global": help_admin[0],
    "restrict": help_admin[1],
    "kang": help_sticker[0],
    "memify": help_sticker[1],
    "memes": help_sticker[2],
    "quotly": help_sticker[3],
    "tiny": help_sticker[4],
}
