import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username}: {user_message}')
    
    if user_message == 'ping':
        await message.channel.send('pong')
    else:
        print('error')

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()
