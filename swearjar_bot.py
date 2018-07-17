#SwearJar_bot by PassTheSoap

import discord
from discord.ext import commands
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='%')
bot_name = "SwearJar_Bot"
bot_game = ""

with open('swears_list', 'r') as swears_file:
    swears_list = swears_file.read()
swears_list = swears_list.split('\n')

@bot.event
async def on_ready():
    print ("Ready to go!")
    await update_bot_game()

@bot.event
async def on_command_error(error, ctx):
    bot.send_message(ctx.message.channel, "The bot has fucked up, somehow. Blame <@ID>")

async def update_bot_game():
    with open('swearjar.json', 'r') as f:
        users_list = json.load(f)
    if 'total' not in users_list:
        bot_game = "Empty!"
    else:
        total = users_list['total']['dollars']
        bot_game = "{} dollars".format(total)
    await bot.change_presence(game=discord.Game(name=bot_game))

@bot.event
async def on_message(message):
    message_split = message.content.split()
    for word in message_split:
        if word.lower() in swears_list:
            await add_dollar_count(message.author)
    await update_bot_game()
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
                await bot.say("**{}** has not put a single dollar in the jar, and is a very good boy. For npw.".format(user_found.name))
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
    with open('info', 'r') as info_file:
        info_str = info_file.read()
    await bot.say(info_str)

@bot.command(pass_context=True)
async def swear(ctx):
    message_split = ctx.message.content.split()
    if len(message_split) > 1:
        await bot.say("""You can only use %swear by itself. Any other arguments will not be taken into account.\nYou also may not put a dollar in the jar in someone else's name.""")
    else:
        await add_dollar_count(ctx.message.author)
        '''emoji = '\N{MONEY BAG}'
        await bot.add_reaction(ctx.message, emoji)'''

async def add_dollar_count(user):
    try:
        with open('swearjar.json', 'r') as f:
            users_list = json.load(f)
            
        if user.id not in users_list:
            users_list[user.id] = {}
            users_list[user.id]['dollars'] = 0
        users_list[user.id]['dollars'] += 1
        if 'total' not in users_list:
            users_list['total'] = {}
            users_list['total']['dollars'] = 0
        users_list['total']['dollars'] += 1
            
        with open('swearjar.json', 'w') as f:
            json.dump(users_list, f)
    except:
        print("Error : couldn't put a dollar in the jar for {}.".format(user.name))

bot.run(os.environ['TOKEN'])
