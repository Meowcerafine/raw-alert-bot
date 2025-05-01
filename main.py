import os
import discord
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Diccionario con todos los webtoons que quieres monitorear
# Formato: "Nombre": "URL"
webtoons = {
    "Lagrimas entre flores marchitas": "https://comic.naver.com/webtoon/list?titleId=827190",
    "Another Series": "https://comic.naver.com/webtoon/list?titleId=000000",  # Cambia estos
}

# Guardamos el último capítulo visto por serie
last_titles = {}

async def check_new_chapters():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        for name, url in webtoons.items():
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')

                latest_episode = soup.select_one('td.title a')
                new_title = latest_episode.text.strip()
                new_link = "https://comic.naver.com" + latest_episode['href']

                # Verifica si ya lo habíamos anunciado
                if last_titles.get(name) != new_title:
                    last_titles[name] = new_title
                    await channel.send(f"📢 ¡Nuevo capítulo de **{name}**!\n**{new_title}**\n🔗 {new_link}")
                else:
                    print(f"No hay nuevo capítulo de {name}.")

            except Exception as e:
                print(f"⚠️ Error al revisar {name}: {e}")

        await asyncio.sleep(600)  # Espera 10 minutos antes de volver a revisar

@client.event
async def on_ready():
    print(f'✅ Conectado como {client.user}')
    await client.get_channel(CHANNEL_ID).send("👀 Monitoreando múltiples series de Naver...")
    client.loop.create_task(check_new_chapters())

client.run(TOKEN)
