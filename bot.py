import os
import discord
from dotenv import load_dotenv

# Retrieve token of bot without exposing token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create intents object with default settings
intents = discord.Intents.default()

# Enable specific intents as needed:
intents.messages = True  # Listen to messages
intents.guilds = True    # Know about guild (server) updates

# Initialize the client with the specified intents
client = discord.Client(intents=intents)

# Run the bot
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)