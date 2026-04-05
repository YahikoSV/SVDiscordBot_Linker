# This example requires the 'message_content' intent.

import discord #discord python library
from discord import app_commands  #discord commands
from discord.ext import tasks, commands  #discord commands
import os #get env file
from playwright.async_api import async_playwright, expect #headless browsing
import random #random choice
import webserver 
from dotenv import load_dotenv  #load env file
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='~', case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): #Happens when prefix is nothing
        return  # Ignore the error quietly
    raise error  # Propagate other errors to the console

@bot.command(name='大きな')
async def shymm(ctx):
    await ctx.send('すきだよ！')

@bot.command(name='live?')
async def check_yt_live(ctx, yt_name):
    start_time = time.time()
    msg = await ctx.send(f'Looking for {yt_name}...')
    result, time1, time2, time3 = await main(yt_name, start_time)
    await msg.delete()
    await ctx.send(result)
    time4 = round(start_time - time.time(),2) #discord time
    await ctx.send(f'{time1},{time2},{time3},{time4}')

@bot.command(name='fbkcat', help='Responds with a random quote from Fubuki')
async def Fubuki_Cat(ctx):
    Fubuki_quotes = [
        'No no cat! I\'m Fox', 
        'Kitsune jyaa!', 
        'Nyaajyanee yo!'
    ]
    response = random.choice(Fubuki_quotes)
    await ctx.send(response)

async def main(yt_name,start_time):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
                headless = True
                ,args=["--blink-settings=imagesEnabled=false"])
        page = await browser.new_page()
        time1 = round(time.time() - start_time,2) #loading chromium
        await page.goto(f"https://www.youtube.com/@{yt_name}")

        try: 
            await expect(page.get_by_role("button", name="Tap to watch live")).to_be_visible(timeout=20000)  
            time2 = round(time.time() - start_time,2) #live is visible
            await page.get_by_role("button", name="Tap to watch live").click()
            time3 = round(time.time() - start_time,2) #stream page
            response = page.url
        except AssertionError as e:
            response = f'{yt_name} is not live'
            time2 = round(time.time() - start_time,2)
            time3 = round(time.time() - start_time,2)
        return response, time1, time2, time3
    
webserver.keep_alive()
bot.run(TOKEN)

