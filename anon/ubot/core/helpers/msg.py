from ubot.utils.dbfunctions import get_var


class Emo:
    def __init__(self, user_id):
        self.user_id = user_id

    async def initialize(self):
        self.ping_var = await get_var(self.user_id, "emo_ping") or "5377321160788684946"
        self.emo_ping = (
            self.ping_var if isinstance(self.ping_var, int) else str(self.ping_var)
        )

        self.pong_var = await get_var(self.user_id, "emo_pong") or "5413739751859566383"
        self.emo_pong = (
            self.pong_var if isinstance(self.pong_var, int) else str(self.pong_var)
        )

        self.proses_var = (
            await get_var(self.user_id, "emo_proses") or "5974326532670230199"
        )
        self.emo_proses = (
            self.proses_var
            if isinstance(self.proses_var, int)
            else str(self.proses_var)
        )

        self.sukses_var = (
            await get_var(self.user_id, "emo_sukses") or "5021905410089550576"
        )
        self.emo_sukses = (
            self.sukses_var
            if isinstance(self.sukses_var, int)
            else str(self.sukses_var)
        )

        self.gagal_var = (
            await get_var(self.user_id, "emo_gagal") or "5019523782004441717"
        )
        self.emo_gagal = (
            self.gagal_var if isinstance(self.gagal_var, int) else str(self.gagal_var)
        )

        self.profil_var = (
            await get_var(self.user_id, "emo_profil") or "5373012449597335010"
        )
        self.emo_profil = (
            self.profil_var
            if isinstance(self.profil_var, int)
            else str(self.profil_var)
        )

        self.alive_var = (
            await get_var(self.user_id, "emo_alive") or "5240141361348360527"
        )
        self.emo_alive = (
            self.alive_var if isinstance(self.alive_var, int) else str(self.alive_var)
        )

    @property
    def ping(self):
        if isinstance(self.emo_ping, int):
            return f"<emoji id={self.emo_ping}>🏓</emoji>"
        else:
            return f"{self.emo_ping}"

    @property
    def pong(self):
        if isinstance(self.emo_pong, int):
            return f"<emoji id={self.emo_pong}>🥵</emoji>"
        else:
            return f"{self.emo_pong}"

    @property
    def proses(self):
        if isinstance(self.emo_proses, int):
            return f"<emoji id={self.emo_proses}>🔄</emoji>"
        else:
            return f"{self.emo_proses}"

    @property
    def sukses(self):
        if isinstance(self.emo_sukses, int):
            return f"<emoji id={self.emo_sukses}>✅</emoji>"
        else:
            return f"{self.emo_sukses}"

    @property
    def gagal(self):
        if isinstance(self.emo_gagal, int):
            return f"<emoji id={self.emo_gagal}>❌</emoji>"
        else:
            return f"{self.emo_gagal}"

    @property
    def profil(self):
        if isinstance(self.emo_profil, int):
            return f"<emoji id={self.emo_profil}>👤</emoji>"
        else:
            return f"{self.emo_profil}"

    @property
    def alive(self):
        if isinstance(self.emo_alive, int):
            return f"<emoji id={self.emo_alive}>⭐</emoji>"
        else:
            return f"{self.emo_alive}"


"""
class Emo:
    def __init__(self, user_id):
        self.prem = self.me.is_premium
        self.user_id = user_id

    async def initialize(self):
        if self.prem == True:
            self.ping_var = await get_var(self.user_id, "emo_ping") or "5269563867305879894"
            self.emo_ping = self.ping_var if self.is_premium else self.ping_var
        
            self.pong_var = await get_var(self.user_id, "emo_pong") or "6183961455436498818"
            self.emo_pong = self.pong_var if self.is_premium else self.pong_var
        
            self.proses_var = await get_var(self.user_id, "emo_proses") or "5974326532670230199"
            self.emo_proses = self.proses_var if self.is_premium else self.proses_var
        
            self.sukses_var = await get_var(self.user_id, "emo_sukses") or "5021905410089550576"
            self.emo_sukses = self.sukses_var if self.is_premium else self.sukses_var
        
            self.gagal_var = await get_var(self.user_id, "emo_gagal") or "5019523782004441717"
            self.emo_gagal = self.gagal_var if self.is_premium else self.gagal_var
        elif self.prem == False:
            self.ping_var = await get_var(self.user_id, "emo_ping") or "🏓"
            self.emo_ping = self.ping_var
        
            self.pong_var = await get_var(self.user_id, "emo_pong") or "🥵"
            self.emo_pong = self.pong_var
        
            self.proses_var = await get_var(self.user_id, "emo_proses") or "🔄"
            self.emo_proses = self.proses_var
        
            self.sukses_var = await get_var(self.user_id, "emo_sukses") or "✅"
            self.emo_sukses = self.sukses_var
        
            self.gagal_var = await get_var(self.user_id, "emo_gagal") or "❌"
            self.emo_gagal = self.gagal_var

    @property
    def ping(self):
        if self.prem == True:
            return f"<emoji id={self.emo_ping}>🏓</emoji>"
        elif self.prem == False:
            return f"{self.emo_ping}"

    @property
    def pong(self):
        if self.is_premium:
            return f"<emoji id={self.emo_pong}>🥵</emoji>"
        elif self.prem == False:
            return f"{self.emo_pong}"

    @property
    def proses(self):
        if self.is_premium:
            return f"<emoji id={self.emo_proses}>🔄</emoji>"
        elif self.prem == False:
            return f"{self.emo_proses}"

    @property
    def sukses(self):
        if self.is_premium:
            return f"<emoji id={self.emo_sukses}>✅</emoji>"
        elif self.prem == False:
            return f"{self.emo_sukses}"

    @property
    def gagal(self):
        if self.is_premium:
            return f"<emoji id={self.emo_gagal}>❌</emoji>"
        elif self.prem == False:
            return f"{self.emo_gagal}"
"""
