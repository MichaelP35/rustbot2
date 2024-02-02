import os
import discord
import features
from dotenv import load_dotenv


# Retrieve token of bot without exposing token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Create intents object with default settings
intents = discord.Intents.default()


# Enable specific intents as needed:
intents.message_content = True  # Listen to messages


# Initialize the client with the specified intents
client = discord.Client(intents=intents)


# Run the bot
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$inspire'):
        quote = features.get_quote()
        await message.channel.send(quote)
    

client.run(TOKEN)