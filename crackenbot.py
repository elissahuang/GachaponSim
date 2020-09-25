import os 
import discord
from discord.utils import get

from dotenv import load_dotenv

TOKEN = os.environ.get('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)