import discord

from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.stickers = []
    
    @commands.command()
    async def balls(self, ctx):
        if not self.stickers:
            self.stickers = ctx.guild.stickers
        
        await ctx.send(stickers=[self.stickers[7]])
