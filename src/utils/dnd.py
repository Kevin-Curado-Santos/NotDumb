import discord 
import random
from discord.ext import commands
import yt_dlp
import d20

ffmpeg_opt = {'options': '-vn'}
ydl_opt = {'format': 'bestaudio', 'verbose': True, 'extractor_args': {"youtube": {"player_client": ["android", "web"]}}}


class Dndbot(commands.Cog):
    def __init__(self, client):
        self.client = client 
        with yt_dlp.YoutubeDL(ydl_opt) as ydl:
            info = ydl.extract_info(f"ytsearch:Rolling Dice - Sound Effect (HD)", download=True)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info['title']
            # source = await discord.FFmpegOpusAudio.from_probe(url, **ffmpeg_opt)
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            self.dice_sound_source = discord.FFmpegPCMAudio(url, before_options=before_options)


    @commands.command()
    async def roll(self, ctx, *, expr = None):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel:
            if not ctx.voice_client:
                await voice_channel.connect()

            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(discord.FFmpegPCMAudio("Rolling Dice - Sound Effect (HD) [rVjCSaXhZTs].webm"))

        if expr == None:
            roll = random.randint(1, 20)
            if roll == 1 or roll == 20:
                embedVar = discord.Embed(title=f'{"Unlucky!" if roll == 1 else "Lucky!"}', color=0x00ff00)
                embedVar.add_field(name=f'You rolled a nat `{roll}`', value='')
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title='d20 Roll', color=discord.Color.random())
                embedVar.add_field(name=f'You rolled a `{roll}`', value='')
                await ctx.send(embed=embedVar)
        else:
            result = d20.roll(expr)

            embedVar = discord.Embed(title=f'{expr} roll', color=discord.Color.random())
            embedVar.add_field(name=f'You rolled {result.total}', value=str(result))
            await ctx.send(embed=embedVar)



