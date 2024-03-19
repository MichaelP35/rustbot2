import os
import random
import features
import discord
import time
import datetime
import re
from discord.ext import commands
from dotenv import load_dotenv


# Retrieve token of bot without exposing token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Create intents object with default settings
intents = discord.Intents.default()


# Enable specific intents:
intents.message_content = True  # Listen to messages
intents.members = True # Listen to members (users)


# Set command prefix and intents
bot = commands.Bot(command_prefix='r!', intents=intents)


# Print to console when bot is ready
@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')


# Basic "Hello, World" message from the bot
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello, World!')


# Say a inspirational quote from Zenquotes.io
@bot.command(name='inspire')
async def inspire(ctx):
    quote = features.get_quote()
    await ctx.send(quote)


# Post a random image of a cat from cataas.com
@bot.command(name='cat')
async def cat(ctx, num: int=1):
    # Discord.py uses lists for multiple file uploads in one message
    cat_images = []

    # Prevents abuse of the command
    if num > 9:
        await ctx.send("Can only generate up to 9 images. Command Aborted!")
    else:
        features.getCatImage(num)
        for i in range(num):
            files = f'images/cat{i}.jpeg'
            cat_images.append(discord.File(files))
        await ctx.send(files=cat_images)


# Guess the number game where the user
# need to guess from 1 to 10
@bot.command(name='guess')
async def guess(ctx):
    await ctx.send('Guess a number from 1 to 10!')

    # Ensure that the user who responded the command
    # is the one who only can answer
    def check(message):
        return message.channel == ctx.channel and message.author == ctx.author
    
    # Generate a number from 1 to 10
    number = random.randint(1, 10)

    # Tell the user if they are right or wrong, and stop the command if
    # they take more than 20 seconds to respond
    try:
        guess = await bot.wait_for('message', check=check, timeout=20.0)

        if guess.content.isdigit():
            user_guess = int(guess.content)
            if user_guess == number:
                await ctx.send('Correct!')
            else:
                await ctx.send(f'Wrong! Correct number is {number}.')
    
    # Opted to just use a generic Exception catch
    # since asyncio.TimeoutError doesn't work
    except Exception:
        await ctx.send('Sorry, you took too long.')


#Convert a given date and time to discord's timestyling
@bot.command(name='time')
async def convert_time(ctx, *, message: str):
    # This pattern will look for a date and time in the message
    date_time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})')
    match = date_time_pattern.search(message)
    
    if match:
        date_str, time_str = match.group().split()
        try:
            # Parse the given date and time
            datetime_obj = datetime.datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
            
            # Convert to UNIX timestamp
            timestamp = int(time.mktime(datetime_obj.timetuple()))
            
            # Replace the date and time in the message with the Discord timestamp style
            new_message = date_time_pattern.sub(f'<t:{timestamp}:F>', message)
            
            # Send the modified message
            await ctx.send(new_message)
        except ValueError:
            # If the date and time are incorrect or in the wrong format, send an error message
            await ctx.send('Invalid date or time format in your message. Please use YYYY-MM-DD for date and HH:MM for time.')
    else:
        # If no date and time were found in the message
        await ctx.send('No valid date and time found in your message. Please include a date and time in YYYY-MM-DD HH:MM format.')



bot.run(TOKEN)