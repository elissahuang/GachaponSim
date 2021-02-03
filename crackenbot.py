import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands
from collections import Counter, OrderedDict
from natsort import natsorted

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!cb ')
index = OrderedDict() # name: month-year

mini = []
mvp = []

@bot.event
async def on_ready():
    print('{bot.user} is now connected.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.errors.ClientException):
        await ctx.send(error)

@bot.command('ping', help='Ping the bot. Are you here?')
# @commands.has_role('true mmo players')
async def ping(ctx):
    await ctx.send('```pongis```')

@bot.command('hellothere')
async def ping(ctx):
    await ctx.send('```General Kenobi```')

@bot.command('list', help='List all currently available gachas.')
# @commands.has_role('true mmo players')
async def list_g(ctx):
    message = await ctx.send('Fetching list of gachas...')
    f = open('Gachas/index.txt', 'r')
    s = '```Here is the list of all currently available gacha.\n'
    i = 1
    for line in f:
        c = line.strip().split(':') # month-year:name
        index[c[1].strip()] = c[0]
        fm = str(i) + ". " + c[0] + " " + c[1] + '\n'
        s = s + fm
        i += 1
    f.close()
    s = s + '```'
    await message.edit(content=s)

@bot.command('preview', help="Preview the selected month's gacha")
# @commands.has_role('true mmo players')
async def preview(ctx, gacha_num: int): 
    message = await ctx.send('Fetching gacha...')
    if not index:
        f = open('Gachas/index.txt', 'r')
        for line in f:
            c = line.strip().split(':') # month-year:name
            index[c[1].strip()] = c[0]
        f.close()
    index_list = list(index.items())
    if gacha_num > len(index_list) or gacha_num < 1:
        await message.edit(content='Gacha not found.')
    else:
        wanted = index_list[gacha_num - 1]
        path = 'Gachas/' + str(wanted[1]) + '-Gacha.txt'
        s = '```' + wanted[0] + ' ' + wanted[1] + '\n'
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
        s = s + '```'
        await message.edit(content=s)

@bot.command('roll', help = "Roll for a selected headwear gacha")
# @commands.has_role('true mmo players')
async def roll(ctx, gacha_num: int, roll_num=1): 
    message = await ctx.send('Rolling...')
    if roll_num > 100 or roll_num < 1:
        await message.edit(content='y u do dis\nhttps://tenor.com/view/stop-it-get-some-help-gif-7929301')
    else:
        if not index:
            f = open('Gachas/index.txt', 'r')
            for line in f:
                c = line.strip().split(':') # month-year:name
                index[c[1].strip()] = c[0]
            f.close()
        index_list = list(index.items())
        if gacha_num > len(index_list) or gacha_num < 1:
            await message.edit(content='Gacha not found.')
        else:
            wanted = index_list[gacha_num - 1]
            path = 'Gachas/' + wanted[1] + '-Gacha.txt'
            f = open(path)
            next(f)
            next(f)

            weight_list = []
            roll_list = []

            for line in f:
                p, n = line.strip().split(':')
                n = n.replace('_', ' ')
                p = int(float(p) * 100)
                n = str(p) + '% ' + n
                weight_list.append(p)
                roll_list.append(n)
            f.close()

            roll_out = random.choices(roll_list, weights=weight_list, k=roll_num)
            
            if roll_num == 1:
                ret = '```GET ' + roll_out[0] + ' x1```'
                await message.edit(content=ret)
            else:
                results = dict(Counter(roll_out))
                ret = '```Results from ' + wanted[0] + ' ' + wanted[1] + ' rolling ' + str(roll_num) + ' times:\n'
                for k in natsorted(results):
                    ret = ret + k + ': ' + str(results[k]) + '\n'
                ret = ret + 'BCC Spent: ' + str(roll_num * 30) + '\n'
                ret = ret + 'USD Wasted: $' + str(roll_num * 30 / 6) + '```'
                await message.edit(content=ret)

# @bot.command('eb', help = 'Roll for the Christmas Eve Wish II box')
# async def eb(ctx, roll_num=1):
#     message = await ctx.send('Rolling...')
#     path = 'Gachas/xmas-2020.txt'
#     f = open(path)
#     next(f)

#     a, b = line.strip().split(':')
#     a = int(float(a) * 100)


#     for line in f:
#         p, n = line.strip().split(':')
#         n = n.replace('_', ' ')

# @bot.command('rr', help = "Roll for this month's costume gacha")
# async def rr(ctx):
#     message = await ctx.send('Rolling...')
#     path = 'Gachas/Monthly-Gacha.txt'
#     f = open(path)

#     weight_list = []
#     roll_list = []

#     for line in f:
#         p, n = line.strip().split(':')
#         n = n.replace('_', ' ')
#         p = int(float(p) * 100)
#         n = str(p) + '% ' + n
#         weight_list.append(p)
#         roll_list.append(n)
#     f.close()

#     roll_out = random.choices(roll_list, weights=weight_list, k=1)

#     ret = '```GET ' + roll_out[0] + ' x1```'
#     await message.edit(content=ret)

# def bossroll():
#     r = random.choices(['mvp', 'mini'], weights=[21.6, 78.4], k=1)
#     card = ''
#     f = open('Gachas/boss.txt')
#     s = f.readline()
#     mini = s.strip().split(',')
#     s = f.readline()
#     mvp = s.strip().split(',')
#     f.close()
#     if r[0] == 'mini':
#         card = random.choice(mini)
#     else:
#         card = random.choice(mvp)
#     return card

@bot.command('bossroll', help="Roll for Combined Fate (MVP/Mini card)")
async def bossroll(ctx, *args):
    message = await ctx.send("Rolling...")
    if len(args) == 0:
        await message.edit(content="Please enter an MVP or Mini monster.")
    # Extracting wanted card
    elif len(args) > 0:
        wanted_card = args[0]
        if len(args) > 1:
            for i in range(1, len(args)):
                wanted_card = wanted_card + " " + args[i]
        r = random.choices(['mvp', 'mini'], weights=[21.6, 78.4], k=1)
        card = ''
        f = open('Gachas/boss.txt')
        s = f.readline()
        mini = s.strip().split(',')
        s = f.readline()
        mvp = s.strip().split(',')
        f.close()

        if wanted_card not in mini and wanted_card not in mvp:
            await message.edit(content="```That is not a valid MVP or MINI monster.```")
        else:
            count = 1
            flag = False
            while (flag == False):
                if r[0] == 'mini':
                    card = random.choice(mini)
                else:
                    card = random.choice(mvp)

                if card == wanted_card:
                    flag = True
                    await message.edit(content="```It took you " + str(count) + " rolls to get " + wanted_card + " Card.```")
                if count > 500:
                    flag = True
                    await message.edit(content="```You did not get the card in 1000 rolls.```")
                else:
                    count += 1
    else:
        await message.edit(content="```An error occurred.```")

@bot.command('broccoli', help="Roll for Combined Fate (MVP/Mini card)")
async def boss(ctx):
    message = await ctx.send("```GET 28% Small Cracken x1```")

@bot.command('boss', help="Roll for Combined Fate (MVP/Mini card)")
async def boss(ctx):
    message = await ctx.send("Rolling...")
    r = random.choices(['mvp', 'mini'], weights=[21.6, 78.4], k=1)
    card = ''
    f = open('Gachas/boss.txt')
    s = f.readline()
    mini = s.strip().split(',')
    s = f.readline()
    mvp = s.strip().split(',')
    f.close()
    if r[0] == 'mini':
        card = '```' + random.choice(mini) + ' Card```'
    else:
        card = '```' + random.choice(mvp) + ' Card```'
    await message.edit(content=card)

bot.run(TOKEN)
