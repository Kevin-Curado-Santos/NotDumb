import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

from utils.commands import Music

discord.utils.setup_logging()

load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
        command_prefix=commands.when_mentioned_or('!'),
        intents=intents,
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

#async def on_message(message):
#    if message.author == bot.user:
#        return 
#    
#    username = str(message.author)
#    user_message = message.content
#    channel = str(message.channel)
#
#    print(f'[{channel}] {username}: {user_message}')
#    
#    if user_message == 'ping':
#        await message.channel.send('pong')


async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())