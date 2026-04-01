# This example requires the 'message_content' intent.

import discord #discord python library
import os #get env file

from dotenv import load_dotenv  #load env file

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('大きな'):
        await message.channel.send('すきだよ！')
print(TOKEN)
client.run(TOKEN)
