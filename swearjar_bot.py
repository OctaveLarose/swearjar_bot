#SwearJar_bot by PassTheSoap

import discord
from discord.ext import commands
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='%')
bot_name = "SwearJar_Bot"
bot_game = "being a good bot"

os.chdir(r'C:\Users\Octave\Desktop\Python Discord bot')

@bot.event
async def on_ready():
    print ("Ready to go!")
    await bot.change_presence(game=discord.Game(name=bot_game))

@bot.event
async def on_command_error(error, ctx):
    bot.send_message(ctx.message.channel, "The bot has fucked up, somehow. Blame <@ID>")

@bot.event
async def on_message(message):
    ''
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def total_jar(ctx):
    with open('swearjar.json', 'r') as f:
        users_list = json.load(f)
    if 'total' not in users_list:
        await bot.say("The jar is empty.")
    else:
        total = users_list['total']['dollars']
        string = "The total amount of money in the jar is : **{} ".format(total)
        if total != 1:
            string += "dollars**"
        else:
            string += "dollar**."
        await bot.say(string.format(total))

@bot.command(pass_context=True)
async def check_jar(ctx, user_sent:str = None):
    if user_sent is None:
        await bot.send_message(ctx.message.channel, "Please enter a username.")
    else:
        if user_sent[0:2] == '<@':
            user_sent = user_sent[2:-1]
            user_found = ctx.message.server.get_member(user_sent)
            if ctx.message.server.get_member(user_found.id) is None:
                await bot.send_message(ctx.message.channel, "User could not be found.")
        else:
            user_found = ctx.message.server.get_member_named(name=user_sent)
        if user_found is None:
            await bot.send_message(ctx.message.channel, "User could not be found.")
        elif user_found == bot.user:
            await bot.send_message(ctx.message.channel, "Nice try, friend. But I'm the one who makes the rules here.")
        else:
            with open('swearjar.json', 'r') as f:
                users_list = json.load(f)
            if user_found.id not in users_list:
                await bot.say("**{}** has not put a single dollar in the jar, and is either a very good boy or a liar.".format(user_found.name))
            else:
                total = users_list[user_found.id]['dollars']
                string = "**{}** has put **{} ".format(user_found.name, total)
                if total != 1:
                    string += "dollars**"
                else:
                    string += "dollar**"
                string += " in the jar."
                await bot.say(string.format(total))

@bot.command()
async def info():
    with open(r'C:\Users\Octave\Desktop\Python Discord bot\info', 'r') as info_file:
        info_str = info_file.read()
    await bot.say(info_str)

@bot.command(pass_context=True)
async def swear(ctx):
    await add_dollar_count(ctx.message.author, ctx)  
    emoji = '\N{MONEY BAG}'
    await bot.add_reaction(ctx.message, emoji)

async def add_dollar_count(user, ctx):
    try:
        with open('swearjadr.json', 'r') as f:
            users_list = json.load(f)
            
        if user.id not in users_list:
            users_list[user.id] = {}
            users_list[user.id]['dollars'] = 0
        else:
            users_list[user.id]['dollars'] += 1
            if 'total' not in users_list:
                users_list['total'] = {}
                users_list['total']['dollars'] = 0
            users_list['total']['dollars'] += 1
            
        with open('swearjar.json', 'w') as f:
            json.dump(users_list, f)
    except:
        bot.send_message(ctx.message.channel, "Error : couldn't put a dollar in the jar for {}. Ask soap to fix it.".format(user.name))

with open(r'C:\Users\Octave\Desktop\Python Discord bot\swearjar_token', 'r') as info_file:
        token = info_file.read()
bot.run(token)
