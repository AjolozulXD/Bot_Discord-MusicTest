import settings
import discord
from discord.ext import commands
from bot_logic import gen_pass, flip_coin
import random
import yt_dlp
import os

# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()
# Activar el privilegio de lectura de mensajes
intents.message_content = True
# Crear un bot en la variable bot y transferirle los privilegios
bot = commands.Bot(command_prefix="B", intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

# Comando para saludar
@bot.command()
async def hola(ctx):
    await ctx.send("holis")

# Comando para despedirse
@bot.command()
async def chau(ctx):
    await ctx.send("Adiós, hermos@")

# Comando para generar una contraseña aleatoria
def gen_pass(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

@bot.command()
async def password(ctx):
    await ctx.send(gen_pass(10))

# Comando para tirar una moneda
def flip_coin():
    return random.choice(["Cara", "Cruz"])

@bot.command()
async def coin(ctx):
    await ctx.send(flip_coin())

# Comando especial
@bot.command()
async def ILoveAxolotls(ctx):
    await ctx.send("Awww 😍🥰")

# Comando para tirar dados
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('El formato tiene que ser NdN (ejemplo: 2d6)!')
        return
    
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# Comando para reproducir música desde un enlace de YouTube
@bot.command()
async def play(ctx, url):
    # Verificar si el usuario está en un canal de voz
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        # Conectarse al canal de voz si no está conectado
        if ctx.voice_client is None:
            await channel.connect()
        # Descarga audio del video
        vc = ctx.voice_client
        info = ytdl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(source=url2, executable="C:\\Users\\mauro\\Downloads\\ffmpeg-2024-09-19-git-0d5b68c27c-essentials_build\\bin\\ffmpeg.exe"))
        await ctx.send(f'Reproduciendo: {info["title"]}')
    else:
        await ctx.send("Tienes que estar en un canal de voz para reproducir música.")

@bot.command()
async def disconnect(ctx):
    if ctx.voice_client:  # Verifica si el bot está conectado al canal de voz
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz.")
    else:
        await ctx.send("No estoy conectado a ningún canal de voz.")

# Comando para detener la música
@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Reproducción detenida.")
    else:
        await ctx.send("No se está reproduciendo música.")

# Comando para buscar videos en YouTube
@bot.command()
async def video(ctx, *, query):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    await ctx.send(f"Puedes ver el video aquí: {search_url}")

bot.run("TOKEN")

bot.run(settings["TOKEN"])
