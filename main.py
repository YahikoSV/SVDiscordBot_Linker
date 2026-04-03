# This example requires the 'message_content' intent.

import discord #discord python library
from discord import app_commands  #discord commands
from discord.ext import tasks, commands  #discord commands
import os #get env file
from playwright.async_api import async_playwright #headless browsing
from playwright.sync_api import sync_playwright


from flask import Flask #keep alive
from threading import Thread #keep alive
import asyncio #asynchronous function to run?

from dotenv import load_dotenv  #load env file

app = Flask('')
@app.route('/')
def main():
    return "Your Bot Is Ready"
def run():
    app.run(host="0.0.0.0", port=8000)
def keep_alive():
    server = Thread(target=run)
    server.start()

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='', case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('大きな'):
        await message.channel.send('すきだよ！')

    if message.content.startswith('Is Rigze live?'):
        response = await main()
        await message.channel.send(response)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True)
        page = await browser.new_page()
        await page.goto("https://www.youtube.com/@rigze0925")
        await page.wait_for_timeout(3000)
        if await page.get_by_role("button", name="Tap to watch live").count() == 1:
            await page.get_by_role("button", name="Tap to watch live").click()
            await page.wait_for_timeout(3000)
            response = page.url
        else: 
            response = 'Rigze is not live'
        await browser.close()
        return response


bot.run(TOKEN)

