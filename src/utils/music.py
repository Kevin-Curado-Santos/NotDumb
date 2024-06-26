import discord
from discord.ext import commands
import yt_dlp


ffmpeg_opt = {'options': '-vn'}
ydl_opt = {'format': 'bestaudio', 'verbose': True, 'extractor_args': {"youtube": {"player_client": ["android", "web"]}}}

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("You are not in a voice channel!")
        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(ydl_opt) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url,title))
                await ctx.send(f'Added **{title}** to queue')
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            # source = await discord.FFmpegOpusAudio.from_probe(url, **ffmpeg_opt)
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            source = discord.FFmpegPCMAudio(url, before_options=before_options)
            ctx.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'Now playing **{title}**')
        elif not ctx.voice_client.is_playing():
            await ctx.send("Queue is empty!")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Stopped!")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await ctx.voice_client.disconnect()


