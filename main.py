# This example requires the 'message_content' intent.

import discord #discord python library
from discord import app_commands  #discord commands
from discord.ext import tasks, commands  #discord commands
import os #get env file
from playwright.async_api import async_playwright, expect #headless browsing
import random #random choice
import webserver 
from dotenv import load_dotenv  #load env file


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
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): #Happens when prefix is nothing
        return  # Ignore the error quietly
    raise error  # Propagate other errors to the console


# @bot.event
# async def on_message(message):
#     if message.content.startswith('大きな'):
#         await message.channel.send('すきだよ！')
#  #       await bot.process_commands(message) #https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working

#     if message.content.startswith('Is Rigze live?'):
#         response = await main(yt_name='rigze0925')
#         await message.channel.send(response)
#     await bot.process_commands(message)

# @bot.listen('on_message')
# async def asdf(message):
#     if message.content.startswith('大きな'):
#         await message.channel.send('すきだよ！')    

@bot.command(name='大きな')
async def shymm(ctx):
    await ctx.send('すきだよ！')

@bot.command(name='live?')
async def check_yt_live(ctx, yt_name):
    result = await main(yt_name)
    await ctx.send(result)

@bot.command(name='fbkcat', help='Responds with a random quote from Fubuki')
async def Fubuki_Cat(ctx):
    Fubuki_quotes = [
        'No no cat! I\'m Fox', 
        'Kitsune jyaa!', 
        'Nyaajyanee yo!'
    ]
    response = random.choice(Fubuki_quotes)
    await ctx.send(response)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
async def main(yt_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
                headless = True
                ,args=["--blink-settings=imagesEnabled=false"])
        page = await browser.new_page()
        await page.goto(f"https://www.youtube.com/@{yt_name}")

        try: 
            await expect(page.get_by_role("button", name="Tap to watch live")).to_be_visible(timeout=5000)  
            await page.get_by_role("button", name="Tap to watch live").click()
            response = page.url
        except AssertionError as e:
            response = f'{yt_name} is not live'
        return response
    
webserver.keep_alive()
bot.run(TOKEN)

