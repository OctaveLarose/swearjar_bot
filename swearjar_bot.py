#SwearJar_bot by PassTheSoap

import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix='%')
bot_name = "SwearJar_Bot#2252"
os.chdir(r'C:\Users\Octave\Desktop\Python Discord bot')

@bot.event
async def on_ready():
    print ("Ready to go!")
    print ("My name is " + bot.user.name)
    print ("My ID is " + bot.user.id)

@bot.event
async def on_message(message):
    if message.author.bot != True:
        if "cookie" in message.content:
               await bot.send_message(message.channel, ":cookie:")
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def total_jar(ctx):
    with open('swearjar.json', 'r') as f:
        users = json.load(f)
    if 'total' not in users:
        await bot.say("The jar is empty.")
    else:
        total = users['total']['dollars']
        string = "The total amount of money in the jar is : {}** ".format(total)
        if total != 1:
            string += "dollars**"
        else:
            string += "dollar**."
        await bot.say(string.format(total))

@bot.command(pass_context=True)
async def check_jar(ctx, user_sent):
    pass

@check_jar.error
async def check_jar_on_error(error, ctx):
	await bot.send_message(ctx.message.channel, "User could not be found.")

@bot.command(pass_context=True)
async def info(ctx):
    with open(r'C:\Users\Octave\Desktop\Python Discord bot\info', 'r') as info_file:
        info_str = info_file.read()
    await bot.say(info_str)

@bot.command(pass_context=True)
async def swear(ctx):
    author = ctx.message.author

    with open('swearjar.json', 'r') as f:
        users = json.load(f)

    if author.id not in users:
        users[author.id] = {}
        users[author.id]['dollars'] = 0

    await add_dollar_count(users, ctx.message.author)

    with open('swearjar.json', 'w') as f:
        json.dump(users, f)
    
    emoji = '\N{MONEY BAG}'
    await bot.add_reaction(ctx.message, emoji)

async def add_dollar_count(users, user):
    if not user.id in users:
        print("Error : user not listed")
    else:
        users[user.id]['dollars'] += 1
        if 'total' not in users:
            users['total'] = {}
            users['total']['dollars'] = 0
        users['total']['dollars'] += 1


bot.run("TOKEN")
