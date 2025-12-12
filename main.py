import os
import discord
from discord.ext import commands
import re  # Regex için

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

warnings = {}

# Küfür ve porno kelimeleri (v1) + bazı varyasyonlar regex ile
bad_words_patterns = [
    r"o+r+o+s+p+u", r"p+i+ç", r"m+a+l", r"a+q", r"s+a+l+a+k", r"s+l+a+k",
    r"ö+k+ü+z", r"k+u+ş\s+b+e+y+i+n+l+i", r"am[iı]na", r"yarrak", r"penis",
    r"porno", r"sex", r"sik", r"sikiş", r"bok", r"orosbucocugu",
    r"göt", r"sürtük", r"yarram", r"yarragim", r"amcık", r"taşak", r"daşak",
    r"vagina", r"cock", r"dick", r"pussy", r"anal", r"fisting", r"blowjob",
    r"cum", r"masturbation", r"tits", r"boobs", r"ass", r"whore", r"slut", r"bitch",
    # Taktiksel varyasyonlar
    r"a\s*m\s*i\s*n\s*a", r"s\s*a\s*l\s*a\s*k"
]

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # Küfür veya porno içeriyor mu regex ile kontrol
    if any(re.search(pattern, msg) for pattern in bad_words_patterns):
        try:
            await message.delete()
        except:
            pass

        user = message.author

        if user.id not in warnings:
            warnings[user.id] = 1
        else:
            warnings[user.id] += 1

        warn_count = warnings[user.id]

        if warn_count < 3:
            await message.channel.send(f"{user.mention} **{warn_count}. Uyarıyı aldı!**")
        else:
            await message.channel.send(f"{user.mention} **3. uyarıyı aldı ve susturuldu!**")
            try:
                await user.timeout(discord.utils.utcnow() + discord.timedelta(days=1), reason="Küfür/Porno")
            except:
                await message.channel.send("❌ Bu kullanıcıyı susturmak için yetkim yok!")

    await bot.process_commands(message)

@bot.command()
async def uyarı_sıfırla(ctx, member: discord.Member):
    warnings[member.id] = 0
    await ctx.send(f"{member.mention} kullanıcısının uyarıları sıfırlandı.")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
