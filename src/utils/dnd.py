import discord 
import random

from discord.ext import commands

class Dndbot(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def roll(self, ctx):
        roll = random.randint(1, 20)
        await ctx.send(f'You rolled a {roll}')

