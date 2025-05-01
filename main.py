import os
import discord
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_title = None  # Guardamos el último capítulo visto

async def check_new_chapter():
    global last_title
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        try:
            url = "https://comic.naver.com/webtoon/list?titleId=814543"  # Cambia este por el que quieres
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encuentra el título del capítulo más reciente
            latest_episode = soup.select_one('td.title a')
            new_title = latest_episode.text.strip()
            new_link = "https://comic.naver.com" + latest_episode['href']

            if last_title != new_title:
                last_title = new_title
                await channel.send(f"📢 ¡Nuevo capítulo disponible!\n**{new_title}**\n🔗 {new_link}")
            else:
                print("🔄 No hay nuevo capítulo todavía.")

        except Exception as e:
            print(f"Error al revisar Naver: {e}")

        await asyncio.sleep(600)  # Espera 10 minutos antes de revisar otra vez

@client.event
async def on_ready():
    print(f'✅ Conectado como {client.user}')
    await client.get_channel(CHANNEL_ID).send("👀 Comenzando a monitorear capítulos...")
    client.loop.create_task(check_new_chapter())

client.run(TOKEN)
