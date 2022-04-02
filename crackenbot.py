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
color = 0x28b7c2

mini = []
mvp = []

@bot.event
async def on_ready():
    print('{bot.user} is now connected.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.errors.ClientException):
        await ctx.send(error)

@bot.command('ping', help='Ping the bot. Are you here?', hidden=True)
# @commands.has_role('true mmo players')
async def ping(ctx):
    embed = discord.Embed(title='pong', color=color)
    await ctx.send(embed=embed)

@bot.command('hellothere', hidden=True)
async def ping(ctx):
    embed = discord.Embed(title='General Kenobi', color=color)
    embed.set_thumbnail(url='https://c.tenor.com/QFSdaXEwtBAAAAAC/hello-there-general-kenobi.gif')
    await ctx.send(embed=embed)

@bot.command('list', help='List all currently available gachas')
# @commands.has_role('true mmo players')
async def list_gacha(ctx):
    message = await ctx.send('Fetching list of gachas...')
    f = open('Gachas/index.txt', 'r')
    i = 1
    s = ''
    for line in f:
        c = line.strip().split(':') # month-year:name
        index[c[1].strip()] = c[0]
        fm = str(i) + ". " + c[0] + " " + c[1] + '\n'
        s = s + fm
        i += 1
    f.close()
    embed = discord.Embed(title='Currently Available Gachas', description=s, color=color)
    await message.edit(content=None, embed=embed)

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
        embed = discord.Embed(title='Gacha not found', color=color)
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/ragnarok_gamepedia_en/images/7/7c/Emote_wah.gif/')
        await message.edit(content='', embed=embed)
    else:
        wanted = index_list[gacha_num - 1]
        name =  wanted [0] + ' ' + wanted[1]
        path = 'Gachas/' + str(wanted[1]) + '-Gacha.txt'
        s = ''
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
        embed = discord.Embed(title=name, description=s, color=discord.Color.blue())
        await message.edit(content='', embed=embed)

@bot.command('roll', help = "Roll for a selected headwear gacha")
# @commands.has_role('true mmo players')
async def roll(ctx, gacha_num: int, roll_num=1): 
    message = await ctx.send('Rolling...')
    if roll_num > 100 or roll_num < 1:
        embed = discord.Embed(title='...', description='y u do dis', color=color)
        embed.set_thumbnail(url='https://c.tenor.com/I59BxE--GvsAAAAM/stop-get-some-help.gif')
        await message.edit(content='', embed=embed)
    else:
        if not index:
            f = open('Gachas/index.txt', 'r')
            for line in f:
                c = line.strip().split(':') # month-year:name
                index[c[1].strip()] = c[0]
            f.close()
        index_list = list(index.items())
        if gacha_num > len(index_list) or gacha_num < 1:
            embed = discord.Embed(title='Gacha not found', color=color)
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/ragnarok_gamepedia_en/images/7/7c/Emote_wah.gif/')
            await message.edit(content='', embed=embed)
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
            
            name = ''
            s = ''
            field = ''
            if roll_num == 1:
                name = 'Rolling ' + wanted[0] + ' ' + wanted[1] + ' . . . !'
                s = 'GET **' + roll_out[0] + '** x1'
            else:
                results = dict(Counter(roll_out))
                name = 'Rolling ' + wanted[0] + ' ' + wanted[1] + ' ' + str(roll_num) + ' times:'
                for k in natsorted(results):
                    s += k + ': ' + str(results[k]) + '\n'
                s += '\nBCC Spent: **' + str(roll_num * 30) + '**\n'
                s += 'USD Wasted: **$' + str(roll_num * 30 / 6) + '**\n'
            embed = discord.Embed(title=name, description=s, color=color)
            await message.edit(content='', embed=embed)

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

@bot.command('bossroll', help="Roll for specific Combined Fate (MVP/MINI card)")
async def bossroll(ctx, *args):
    message = await ctx.send("Rolling...")
    if len(args) == 0:
        embed = discord.Embed(title='Please enter an MVP or MINI monster', color=color)
        await message.edit(content='', embed=embed)
    # Extracting wanted card
    elif len(args) > 0:
        wanted_card = args[0]
        if len(args) > 1:
            for i in range(1, len(args)):
                wanted_card = wanted_card + ' ' + args[i]
        r = random.choices(['mvp', 'mini'], weights=[24.9, 75.1], k=1)
        card = ''
        f = open('Gachas/boss.txt')
        s = f.readline()
        mini = s.strip().split(',')
        s = f.readline()
        mvp = s.strip().split(',')
        f.close()

        mini_l = [m.lower() for m in mini]
        mvp_l = [m.lower() for m in mvp]

        if wanted_card.lower() not in mini_l and wanted_card.lower() not in mvp_l:
            embed = discord.Embed(title='That is not a valid MVP or MINI monster', color=color)
            await message.edit(content='', embed=embed)
        else:
            count = 1
            flag = False
            while (flag == False):
                if r[0] == 'mini':
                    card = random.choice(mini)
                else:
                    card = random.choice(mvp)

                if card.lower() == wanted_card.lower():
                    flag = True
                    s = 'It took **' + str(count) + '** rolls to get ' + wanted_card.title() + ' Card'
                    embed = discord.Embed(title='Success!', description=s, color=color)
                    await message.edit(content='', embed=embed)
                if count > 500:
                    flag = True
                    s = 'You did not get the card in 500 rolls'
                    embed = discord.Embed(title='Fail!', description=s, color=color)
                    await message.edit(content='', embed=embed)
                else:
                    count += 1
    else:
        embed = discord.Embed(title='An error occurred', color=color)
        await message.edit(content='', embed=embed)

@bot.command('boss', help="Roll for Combined Fate (MVP/MINI card)")
async def boss(ctx):
    message = await ctx.send("Rolling...")
    r = random.choices(['mvp', 'mini'], weights=[24.9, 75.1], k=1)
    card = ''
    f = open('Gachas/boss.txt')
    s = f.readline()
    mini = s.strip().split(',')
    s = f.readline()
    mvp = s.strip().split(',')
    f.close()
    if r[0] == 'mini':
        card = 'GET **' + random.choice(mini) + '** Card'
    else:
        card = 'GET **' + random.choice(mvp) + '** Card'
    embed = discord.Embed(title='Rolling Combined Fate . . . !', description=card, color=color)
    await message.edit(content='', embed=embed)

@bot.command('broccoli', hidden=True, help="For General Cracken, may he be Bill")
async def broccoli(ctx):
    message = await ctx.send("Contacting General Cracken . . .")
    embed = discord.Embed(title='Rolling Deep Sea Treasure Land 2020-03 . . . !', description='GET **28% Small Cracken** x1', color=color)
    embed.set_thumbnail(url='https://www.romcodex.com/icons/item/item_3001274.png')
    embed.set_footer(text='For General Cracken, may he be Bill')
    await message.edit(content='', embed=embed)

@bot.command('carrot', help='The Great Carrot reaches into the future to find the answers to your questions. It knows what will be and is willing to share this with you')
async def carrot(ctx, *args):
    message = await ctx.send('Contacting The Great Carrot...')
    if len(args) == 0:
        embed = discord.Embed(title='The Great Carrot says . . .', description='Fine keep your secrets. I do not carrot all', color=color)
        await message.edit(content='', embed=embed)
    else:
        responses = [
            'As I see it, yes', 
            'Ask again later', 
            'Better not tell you now', 
            'Cannot predict now', 
            'Concentrate and ask again',
            "Don't count on it",
            'It is certain',
            'It is decidedly so',
            'Most likely',
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Outlook good',
            'Reply hazy, try again',
            'Signs point to yes',
            'Very doubtful',
            'Without a doubt',
            'Yes',
            'Yes - definitely',
            'You may rely on it',
            'I do not carrot all',
            'Inconclusive'
        ]
        s = str(random.choice(responses))
        embed = discord.Embed(title='The Great Carrot says . . .', description=s, color=color)
        await message.edit(content='', embed=embed)

bot.run(TOKEN)
