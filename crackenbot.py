import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from collections import OrderedDict

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!cb ')
index = OrderedDict() # name: month-year

@bot.event
async def on_ready():
    print('{bot.user} is now connected.')

@bot.command('ping', help='Ping the bot. Are you here?')
@commands.has_role('true mmo players')
async def ping(ctx):
    await ctx.send('pong')

@bot.command('list', help='List all currently available gachas.')
@commands.has_role('true mmo players')
async def list_g(ctx):
    await ctx.send('Fetching list of gachas...')
    f = open('Gachas/index.txt', 'r')
    s = 'Here is the list of all currently available gacha.\n'
    i = 1
    for line in f:
        c = line.strip().split(':') # month-year:name
        index[c[1].strip()] = c[0]
        fm = str(i) + ". " + c[0] + " " + c[1] + '\n'
        s = s + fm
        i += 1
    f.close()
    
    await ctx.send(s)

@bot.command('preview', help="Preview the selected month's gacha")
@commands.has_role('true mmo players')
async def preview(ctx, gacha_num: int): 
    await ctx.send('Fetching gacha...')
    if not index:
        f = open('Gachas/index.txt', 'r')
        s = 'Here is the list of all currently available gacha.\n'
        i = 1
        for line in f:
            c = line.strip().split(':') # month-year:name
            index[c[1].strip()] = c[0]
            fm = str(i) + ". " + c[0] + " " + c[1] + '\n'
            s = s + fm
            i += 1
        f.close()
    index_list = list(index.items())
    if gacha_num > len(index_list) or gacha_num < 1:
        await ctx.send('Gacha not found.')
    else:
        wanted = index_list[gacha_num - 1]
        path = 'Gachas/' + str(wanted[1]) + '-Gacha.txt'
        s = wanted[0] + ' ' + wanted[1] + '\n'
        f = open(path)
        next(f)
        next(f)
        for line in f:
            p, n = line.strip().split(':')
            n = n.replace('_', ' ')
            p = float(p) * 100
            p = int(p)
            s = s + str(p) + '% ' + n + '\n'
        f.close()

        await ctx.send(s)




# @bot.command('roll')
# async def roll():

# @bot.command('check')
# async def check():

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)