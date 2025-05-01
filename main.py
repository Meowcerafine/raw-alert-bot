import os
import discord
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Diccionario con las series de Naver a monitorear
naver_series = {
    "Lágrimas por flores marchitas": "https://comic.naver.com/webtoon/list?titleId=827190",
    "En camino a ver a mi madre": "https://m.comic.naver.com/webtoon/list?titleId=834369",
    "El ultimo tren": "https://m.comic.naver.com/webtoon/list?titleId=834896",
    "Probablemente invencible": "https://comic.naver.com/webtoon/list?titleId=834396",
    "La noche de la viuda": "https://series.naver.com/comic/detail.series?productNo=12427989&isWebtoonAgreePopUp=true",
    "Se convirtió en la esposa del lider del culto demoniaco": "https://comic.naver.com/webtoon/list?titleId=837998",
    "La peor generación": "https://comic.naver.com/webtoon/list?titleId=834261",
    "Oxido": "https://comic.naver.com/webtoon/list?titleId=832984", 
    "marca gris": "https://comic.naver.com/webtoon/list?titleId=829462",
    "Por que no deberías entrar en una casa embrujada": "https://comic.naver.com/webtoon/list?titleId=834250",
    "La razón por la que dejé de ser el rey demonio": "https://comic.naver.com/webtoon/list?titleId=820897",
    "Estación de Seúl Bárvara": "https://comic.naver.com/webtoon/list?titleId=832669", 
    "El advenimiento del infierno": "https://comic.naver.com/webtoon/list?titleId=818192",
    "Estrella en la cima": "https://comic.naver.com/webtoon/list?titleId=833679", 
    "Bombero": "https://comic.naver.com/webtoon/list?titleId=833611", 
    "El resurgimiento del caballero a través de manggeom": "https://comic.naver.com/webtoon/list?titleId=833417",
    "Reseña de amor": "https://series.naver.com/comic/detail.series?productNo=12012518",
    "Emperatriz maria": "https://comic.naver.com/webtoon/list?titleId=836785&tab=mon",
    "Registro de trabajo": "https://series.naver.com/comic/detail.series?productNo=12337617",
    "Abrazame fuerte": "https://comic.naver.com/webtoon/list?titleId=837514",
    "Por mi bella julieta": "https://series.naver.com/comic/detail.series?productNo=11469822",
    "Pensé que moriria": "https://series.naver.com/comic/detail.series?productNo=9021824", 
    "Me convertí en el sirviente masculino del duque": "https://comic.naver.com/webtoon/list?titleId=834512",
    "Me casaré en esta vida":"https://series.naver.com/comic/detail.series?productNo=11856507", # Cambia estos
}

# Diccionario con las series de NewToki a monitorear
newtoki_series = {
    "폭군의 침방 시녀가 되었다": "https://newtoki468.com/webtoon/39013833/%ED%8F%AD%EA%B5%B0%EC%9D%98-%EC%B9%A8%EB%B0%A9-%EC%8B%9C%EB%85%80%EA%B0%80-%EB%90%98%EC%97%88%EB%8B%A4?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0",
    "죽음 뒤에 알게 된 것들": "https://newtoki468.com/webtoon/45642634?stx=%EC%A3%BD%EC%9D%8C+%EB%92%A4%EC%97%90+%EC%95%8C%EA%B2%8C+%EB%90%9C+%EA%B2%83%EB%93%A4&title=%EC%A3%BD%EC%9D%8C-%EB%92%A4%EC%97%90-%EC%95%8C%EA%B2%8C-%EB%90%9C-%EA%B2%83%EB%93%A4",
    "Ruegame": "https://newtoki468.com/webtoon/41520458?stx=%EB%82%B4%EA%B2%8C+%EB%B9%8C%EC%96%B4%EB%B4%90&title=%EB%82%B4%EA%B2%8C-%EB%B9%8C%EC%96%B4%EB%B4%90",
}

# Almacenamos el último capítulo revisado por serie
last_titles = {}

async def check_updates():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        # Revisar series de Naver
        for name, url in naver_series.items():
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')

                latest_episode = soup.select_one('td.title a')
                new_title = latest_episode.text.strip()
                new_link = "https://comic.naver.com" + latest_episode['href']

                if last_titles.get(name) != new_title:
                    last_titles[name] = new_title
                    await channel.send(f"📢 ¡Nuevo capítulo de **{name}**!\n**{new_title}**\n🔗 {new_link}")
                else:
                    print(f"No hay nuevo capítulo de {name}.")

            except Exception as e:
                print(f"⚠️ Error al revisar {name} en Naver: {e}")
        
        # Revisar series de NewToki
        for title, url in newtoki_series.items():
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                latest_chap = soup.select_one("div.web_list ul li a")
                chap_title = latest_chap.text.strip()
                chap_link = "https://newtoki468.com" + latest_chap['href']

                if last_titles.get(title) != chap_title:
                    last_titles[title] = chap_title
                    await channel.send(f"📢 ¡Nuevo capítulo de **{title}**!\n**{chap_title}**\n🔗 {chap_link}")
                else:
                    print(f"No hay nuevo capítulo de {title} en NewToki.")

            except Exception as e:
                print(f"⚠️ Error al revisar {title} en NewToki: {e}")

        # Revisar cada 10 minutos
        await asyncio.sleep(600)

@client.event
async def on_ready():
    print(f"✅ Conectado como {client.user}")
    await client.get_channel(CHANNEL_ID).send("👀 Monitoreando capítulos de Naver y NewToki...")
    client.loop.create_task(check_updates())

client.run(TOKEN)

