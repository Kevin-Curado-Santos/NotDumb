
def get_author_voice_channel(ctx):
    return ctx.author.voice.channel if ctx.author.voice else None
