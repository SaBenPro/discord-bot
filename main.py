import os, re, discord, unicodedata
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

warnings = {}

# =========================
# 🧠 AKILLI NORMALIZE
# =========================
def normalize(t: str) -> str:
    t = t.lower()

    # leet + özel karakterler
    t = (t.replace("@","a").replace("1","i").replace("!","i")
           .replace("0","o").replace("$","s").replace("€","e")
           .replace("3","e").replace("4","a").replace("5","s")
           .replace("7","t"))

    # Türkçe -> latin
    tr = str.maketrans("ıİşŞğĞçÇöÖüÜ","iissggccoouu")
    t = t.translate(tr)

    # unicode sadeleştir
    t = unicodedata.normalize("NFKD", t)

    # harf/rakam dışı SİL (boşluk, nokta, emoji, vs)
    t = re.sub(r"[^a-z0-9]", "", t)

    # uzatma kır (oooo → o)
    t = re.sub(r"(.)\1+", r"\1", t)

    return t

# =========================
# 🚫 ÇEKİRDEK KÜFÜRLER
# normalize hepsini yakalar
# =========================
BAD_WORDS = [
    # Türkçe ağır
    "orospu","orospucocugu","am","amina","amcik","yarrak","yarram",
    "sik","sikis","got","tasak","dasak","ibne","pic","salak","mal",
    "gerizekali","aptal","kahpe","serefsiz",

    # Kısaltmalar / argo
    "aq","mk","sg","oc",

    # İngilizce / porno
    "fuck","shit","bitch","whore","slut","ass","dick","cock","pussy",
    "penis","vagina","sex","porno","anal","blowjob","cum","boobs","tits"
]

PATTERNS = [re.compile(w) for w in BAD_WORDS]

# =========================
@bot.event
async def on_ready():
    print(f"🔥 TITAN FILTER AKTIF: {bot.user}")

# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    cleaned = normalize(message.content)

    if any(p.search(cleaned) for p in PATTERNS):
        try:
            await message.delete()
        except:
            pass

        uid = message.author.id
        warnings[uid] = warnings.get(uid, 0) + 1
        w = warnings[uid]

        if w < 3:
            await message.channel.send(
                f"{message.author.mention} ⚠️ **{w}. uyarı!**"
            )
        else:
            await message.channel.send(
                f"{message.author.mention} 🔇 **3. uyarı → 1 gün timeout!**"
            )
            try:
                await message.author.timeout(
                    discord.utils.utcnow() + timedelta(days=1),
                    reason="Küfür / Porno"
                )
            except:
                await message.channel.send("❌ Yetkim yok!")

    await bot.process_commands(message)

# =========================
@bot.command()
async def uyarı_sıfırla(ctx, member: discord.Member):
    warnings[member.id] = 0
    await ctx.send(f"✅ {member.mention} uyarıları sıfırlandı.")

bot.run(os.getenv("TOKEN"))
