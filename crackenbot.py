import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!cb ')
index = {}

@bot.command('ping', help='Ping the bot. Are you here?')
@commands.has_role('true mmo players')
async def ping(ctx):
    await ctx.send('pong')

@bot.command('list', help='List all currently available gachas.')
@commands.has_role('true mmo players')
async def list(ctx):
    await ctx.send('Fetching list of gachas.')
    f = open('gachas/index.txt', 'r')
    s = 'Here is the list of all currently available gacha.\n'
    i = 1
    for line in f:
        c = line.strip().split(':') # month-year:name
        index[c[1].strip()] = c[0]
        fm = str(i) + " " + c[0] + " " + c[1] + '\n'
        s = s + fm
        i += 1
    f.close()
    
    await ctx.send(s)

# @bot.command('preview', help="Preview the select month's gacha")
# @commands.has_role('true mmo players')
# async def preview(ctx):

# @bot.command('roll')
# async def roll():

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)