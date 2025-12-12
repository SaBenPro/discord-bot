import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")

@bot.command()
async def merhaba(ctx):
    await ctx.send("Selam knk! Bot çalışıyor 👋")

TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
