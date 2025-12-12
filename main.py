import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Kullanıcı uyarılarını tutmak için
warnings = {}

# Yasak kelimeler
bad_words = [
    "orospu", "piç", "mal", "aq", "salak", "öküz",
    "kuş beyinli", "amına kodum", "yarrak", "penis", "am"
]

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # Küfür içeriyor mu kontrol et
    if any(word in msg for word in bad_words):
        try:
            await message.delete()  # Mesajı sil
        except:
            pass

        user = message.author

        # Uyarıyı ekle
        if user.id not in warnings:
            warnings[user.id] = 1
        else:
            warnings[user.id] += 1

        warn_count = warnings[user.id]

        # 1-2-3 uyarı mesajları
        if warn_count < 3:
            await message.channel.send(f"{user.mention} **{warn_count}. Uyarıyı aldı!**")
        else:
            # 3. uyarı = Susturma
            await message.channel.send(f"{user.mention} **3. uyarıyı aldı ve susturuldu!**")

            # Kullanıcıyı tüm sunucuda sustur (timeout)
            try:
                await user.timeout(discord.utils.utcnow() + discord.timedelta(days=1), reason="Küfür")
            except:
                await message.channel.send("❌ Bu kullanıcıyı susturmak için yetkim yok!")

    await bot.process_commands(message)


@bot.command()
async def uyarı_sıfırla(ctx, member: discord.Member):
    """Birinin uyarılarını sıfırlar."""
    warnings[member.id] = 0
    await ctx.send(f"{member.mention} kullanıcısının uyarıları sıfırlandı.")


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
