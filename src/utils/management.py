import discord

import requests
import json

from discord.ext import commands

from utils.db import *

info_url = 'https://codeforces.com/api/user.info?handles='
profile_url = 'https://codeforces.com/profile/'

color_ranks = {
        'newbie': 0xAAAAAA,
        'pupil': 0x60FF00,
        'specialist': 0x00DDAA,
        'expert': 0x0000FF,
        'candidate master': 0x7D4BD4,
        'master': 0xFFCC00,
        'international master': 0xFFB400,
        'grandmaster': 0xFF0000,
        'international grandmaster': 0xFF2222,
        'legendary grandmaster': 0xEA0000
        }

def process_rank(resp):
    result = resp.text
    result = json.loads(result)
    result = result["result"]
    return result

class Management(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = connect_users()
        users_table(self.db)

    @commands.command()
    async def register(self, ctx, *, codeforces_name):
        res = store_user(self.db, ctx.author.id, codeforces_name)
        if codeforces_name == '':
            await ctx.send(f"You forgot to provide the codeforces name")
            return
        if res:
            await ctx.send(f"Welcome {codeforces_name}! Ready to duel?")
        else:
            await ctx.send(f"Username updated to {codeforces_name}!")

    @commands.command()
    async def unregister(self, ctx):
        remove_user(self.db, ctx.author.id)
        await ctx.send("Sad to see you go!")

    @commands.command()
    async def crank(self, ctx, *, handles=""):
        query_url = info_url
        if handles == "":
            handle = get_user(self.db, ctx.author.id)
            if handle != None:
                query_url += f"{handle}"
                resp = requests.get(query_url)
                result = process_rank(resp)
                rating = result[0]["rating"]
                rank = result[0]["rank"]
                thumb = result[0]["titlePhoto"]
                emb = discord.Embed(title=handle, color=color_ranks[rank])
                emb.set_thumbnail(url=thumb)
                emb.add_field(name=rank, value=rating, inline=False)
                emb.add_field(name=profile_url+handle, value='', inline=False)
                await ctx.send(embed = emb)
            else:
                await ctx.send('You are not registered! Try using `!register`.')
        else:
            handles = handles.split(' ')
            query_handles = ';'.join(list(set(handles)))
            query_url += f'?{query_handles}'
            resp = requests.get(query_url)
            result = process_rank(resp)
            embs = []
            for i in range(len(result)):
                rating = result[i]["rating"]
                rank = result[i]["rank"]
                thumb = result[i]["titlePhoto"]
                emb = discord.Embed(title=handles[i], color=color_ranks[rank])
                emb.set_thumbnail(url=thumb)
                emb.add_field(name=rank, value=rating, inline=False)
                emb.add_field(name=profile_url+handles[i], value='', inline=False)
                embs.append(emb)
                
            await ctx.send(embeds = embs)
