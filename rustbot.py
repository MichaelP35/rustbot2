import os
import random
import features
import discord
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


# Auto-role upon a member joining the guild
# @bot.event
# async def on_member_join(member):
#     role = "Member"
#     role = discord.utils.get(member.guild.roles, name=role)
#     await member.add_roles(role)
#     print(f'{member} was given the {role} role.')

    
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


# Embed Test
@bot.command(name='embed')
async def EmbedTest(ctx):
    embed = discord.Embed(title='Test')
    await ctx.send(embed=embed)



bot.run(TOKEN)