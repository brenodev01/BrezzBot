import discord
from discord.ext import commands, tasks
from datetime import time
import asyncio
import yt_dlp

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot ligado")

@bot.event
async def on_member_join(mbr:discord.Member):
    channel = bot.get_channel(1387770520338174062)
    bem_vindo = discord.Embed()
    bem_vindo.title = "Seja bem vindo ao servidor!"
    bem_vindo.description = f'Olá {mbr.mention} seja bem vindo não se esqueça de ler as regras em:<#{1387652100233756744}> e fazer seu registro em <#{1387663325029990440}>' 
    image = discord.File("Imagens/BemVindoBreezBot.gif", "BemVindo.gif" )
    thumbnail = discord.File("Imagens/BabyYoda.jpeg", "BabyYoda.jpeg")
    bem_vindo.color = 0xff0000
    bem_vindo.set_thumbnail(url= "attachment://BabyYoda.jpeg")
    bem_vindo.set_image(url= "attachment://BemVindo.gif")
    await channel.send(embed=bem_vindo, files = [image, thumbnail])

queue = []

# !play <nome ou link>
@bot.command()
async def play(ctx, *, search: str):
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if not voice_channel:
        await ctx.send("⚠️ Você precisa estar em um canal de voz!")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client or not voice_client.is_connected():
        voice_client = await voice_channel.connect()

    song = await get_song_url(search)
    queue.append(song)

    if not voice_client.is_playing():
        await play_music(ctx, voice_client)

async def play_music(ctx, voice_client):
    while queue:
        url = queue.pop(0)
        with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        source = await discord.FFmpegOpusAudio.from_probe(audio_url, method='fallback')
        voice_client.play(source)

        await ctx.send(f"🎶 Tocando agora: {info['title']}")
        while voice_client.is_playing():
            await asyncio.sleep(1)

# !stop
@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        queue.clear()
        await ctx.send("⛔ Música parada e bot saiu da call!")

# !next
@bot.command()
async def next(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("⏭️ Pulando para a próxima...")

async def get_song_url(search):
    ydl_opts = {'format': 'bestaudio', 'quiet': True, 'default_search': 'ytsearch1'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        return info['entries'][0]['webpage_url'] if 'entries' in info else info['webpage_url']




































bot.run("MTM4Nzc2NDg4MDQzNzgwOTIyMg.GtTukT.vM8MHVT1iOfy8NcQgSL5ledluXdzBG4VkmENiA")