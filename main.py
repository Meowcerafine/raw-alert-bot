import discord
import os
from discord.ext import tasks

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    check_updates.start()

@tasks.loop(minutes=60)  # cada hora
async def check_updates():
    # Aquí puedes hacer scraping a Naver o NewToki
    # Por ahora, solo envía un mensaje de prueba
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🔔 ¡Revisa si hay nuevo capítulo!")

client.run(TOKEN)
