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


class TimedUser:

    def __init__(self, user, timeout_mins = 60):
        self.user = user
        now = time.time()
        self.timeout = now + (timeout_mins * 60)

    def get_remaining_time(self):
        return int((self.timeout - time.time()) / 60)


@bot.command(pass_context=True, description='Who wants to play?')
async def who(ctx):
    """List waiting players."""
    if timed_users:
        print_str = 'There are ' + str(len(timed_users)) + ' people waiting to play dota\n' 
        for user in timed_users:
            print_str += user.user.name + ' - ' + str(user.get_remaining_time()) + ' minutes\n'
        await bot.say(print_str)
    else:
        await bot.say("No one wants to play Dota right now.")


@bot.command(description='Alert players.')
async def alert():
    """Send @mentions to everyone in the !who list."""
    print_str = 'go ' 
    for user in timed_users:
        print_str += user.user.mention + ' '
    await bot.say(print_str)


@bot.command(pass_context=True,description='Play some Dota!')
async def dota(ctx, time : int = 60):
    """Add or remove yourself from the list of waiting players.
	   Optional time parameter in minutes.
	   e.g. !dota 60"""
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

			
bot.loop.create_task(check_timers())
# client.loop.create_task(print_who())
bot.run('MzA5NzAyNzY3NjEyNzg4NzQ2.DBidow.VGf7Wrc60J0iUzTLGyNTFWfpQQc')



