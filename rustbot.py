import os
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


# Post a random image of a cat
@bot.command(name='cat')
async def cat(ctx):
    features.getCatImage()
    file = 'cat.jpeg'
    await ctx.send(file=discord.File(file))
    os.remove(file)


bot.run(TOKEN)