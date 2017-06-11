import discord
import aiohttp
import asyncio
import logging
import time
from discord.ext import commands

description = 'A discord bot'

bot = commands.Bot(command_prefix='!', description=description)

# Initialize logging
logging.basicConfig(level=logging.INFO)

timed_users = []

# client = discord.Client()
dota_channel = discord.Object(id='89274408438353920')
bot_channel = discord.Object(id='321781885699358741')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def if_user_available_remove(user):
    for auser in timed_users:
        if auser.user == user:
            timed_users.remove(auser)
            return True
    return False

# async def print_who():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         await who(channel)
#         await asyncio.sleep(60)

async def check_timers():
    await bot.wait_until_ready()
    while not bot.is_closed:
        now = time.time()
        for user in timed_users:
            if now > user.timeout:
                print("User timed out: " + user.user.name)
                timed_users.remove(user)
                await bot.say(user.user.name + ' is no longer playing (' + str(len(timed_users)) + '/5) -timeout')
        await asyncio.sleep(20)


# async def msg_format():
#     async with aiohttp.get('https://discordapp.com/api/channels/321781885699358741/messages') as r:
#         js = await r.json()
#         print(str(r.status))
#         print(js)
#             # await client.send_message(channel, js['file'])

class TimedUser:

    def __init__(self, user, timeout_mins = 60):
        self.user = user
        now = time.time()
        self.timeout = now + (timeout_mins * 60)

    def get_remaining_time(self):
        return int((self.timeout - time.time()) / 60)


@bot.command(pass_context=True)
async def who(ctx):
    if timed_users:
        print_str = 'There are ' + str(len(timed_users)) + ' people waiting to play dota\n' 
        for user in timed_users:
            print_str += user.user.name + ' - ' + str(user.get_remaining_time()) + ' minutes\n'
        await bot.say(print_str)
    else:
        await bot.say("No one wants to play Dota right now.")


@bot.command()
async def alert():
    print_str = 'go ' 
    for user in timed_users:
        print_str += user.user.mention + ' '
    await bot.say(print_str)


@bot.command(pass_context=True)
async def dota(ctx, time : int = 60):
    user = ctx.message.author

    if if_user_available_remove(user):
        await bot.send_message(bot_channel, user.name + ' is no longer playing (' + str(len(timed_users)) + '/5)')
    else:
        try:
            new_player = TimedUser(user, time)
        except Exception:
            bot.say("Wrong type for timeout minutes")
            return
        timed_users.append(new_player)
        await bot.say(user.name + ' is up to play Dota! (' + str(len(timed_users)) + '/5)')

        if len(timed_users) == 5:
            await alert()


# @bot.event
# async def on_message(message):
#     user = message.author
#
#     if message.content.startswith('!dota'):
#         if if_user_available_remove(user):
#             # await bot.say(bot_channel, user.name + ' is no longer playing (' + str(len(timed_users)) + '/5)')
#         else:
#             splitted_msg = message.content.split(' ')
#             if len(splitted_msg) == 1:
#                 new = TimedUser(user, 60)
#                 timed_users.append(new)
#                 # await bot.say(bot_channel, '{0} is up to play dota ({1}/5)'.format(user.name, str(len(timed_users))))
#             elif len(splitted_msg) == 2:
#                 #Check if given timeout duration is an integer
#                 if splitted_msg[1].isdigit():
#                     new = TimedUser(user, int(splitted_msg[1]))
#                     timed_users.append(new)
#                     await bot.say(bot_channel, user.name + ' is up to play Dota for ' + str(splitted_msg[1])+ ' minutes! (' + str(len(timed_users)) + '/5)')
#                 else:
#                     await bot.say(bot_channel, 'Wrong type for timeout minutes.')
#
#             if len(timed_users) == 5:
#                 await alert()
#
#     # elif message.content.startswith('!who'):
#     #     await who(message.channel)
#
#     # elif message.content.startswith('!alert'):
#     #     await alert()
#     #
#     # elif message.content.startswith('!ilker'):
#     #     print(user.name + " ilker'd")
#     #     await bot.delete_message(message)
#     #
#     # elif message.content.startswith('!delete'):
#     #     await bot.delete_message(message)
#     #     print("Deleted message: " + message.content)
#
#     # elif message.content.startswith('!msg'):
#     #     await msg_format()
#
#     elif message.content.startswith('!help'):
#         await bot.say(bot_channel, "Commands for dotobot:\n\n" +
#                                                    "!dota - toggle dota availability (now with timeout!)\n" +
#                                                    "!who - print people up to play dota\n" +
#                                                    "!alert - alert people who want to play dota\n" +
#                                                    "!ilker - delete this message\n" +
#                                                    "!help - print this help")



bot.loop.create_task(check_timers())
# client.loop.create_task(print_who())
bot.run('MzA5NzAyNzY3NjEyNzg4NzQ2.DBidow.VGf7Wrc60J0iUzTLGyNTFWfpQQc')



