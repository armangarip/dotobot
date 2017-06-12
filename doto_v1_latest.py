import discord
import aiohttp
import asyncio
import logging
import time
import config
from discord.ext import commands

description = 'A discord bot'

bot = commands.Bot(command_prefix='!', description=description)

# Initialize logging
logging.basicConfig(level=logging.INFO)

timed_users = []

#Read Config
conf = config.getConfig()
DOTA_CHANNEL_ID = conf['CHANNELS']['DotaChannelID']
BOT_CHANNEL_ID = conf['CHANNELS']['BotChannelID']
BOT_TOKEN = conf['BOT']['token']
ALERT_TEXT = conf['DEFAULT_VALUES']['alertText']

try:
    TIMEOUT_DEFAULT = int(conf['DEFAULT_VALUES']['timeout'])
except ValueError:
    TIMEOUT_DEFAULT = 60

# client = discord.Client()
if not DOTA_CHANNEL_ID:
    print('Missing Dota channel id!')
dota_channel = discord.Object(id=DOTA_CHANNEL_ID)

if not BOT_CHANNEL_ID:
    print('Missing Bot channel id!')
bot_channel = discord.Object(id=BOT_CHANNEL_ID)


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
        for timed_user in timed_users:
            if now > timed_user.timeout:
                print("User timed out: " + timed_user.user.name)
                timed_users.remove(timed_user)
                await bot.say(timed_user.user.name + ' is no longer playing (' + str(len(timed_users)) + '/5) -timeout')
        await asyncio.sleep(20)


class TimedUser:

    def __init__(self, user, timeout_mins = 60, note = ''):
        self.user = user
        now = time.time()
        self.timeout = now + (timeout_mins * 60)
        self.note = note

    def get_remaining_time(self):
        return int((self.timeout - time.time()) / 60)


@bot.command(pass_context=True, description='Who wants to play?')
async def who(ctx):
    """List waiting players."""
    if timed_users:
        print_str = 'There are ' + str(len(timed_users)) + ' people waiting to play dota\n' 
        for timed_user in timed_users:
            print_str += timed_user.user.name + ' - ' + str(timed_user.get_remaining_time()) + ' minutes'
            if len(timed_user.note) > 0 :
                print_str += ' - "' + timed_user.note + '"'
            print_str += '\n'
        await bot.say(print_str)
    else:
        await bot.say("No one wants to play Dota right now.")


@bot.command(description='Alert players.')
async def alert():
    """Send @mentions to everyone in the !who list."""
    print_str = ALERT_TEXT + ' ' 
    for timed_user in timed_users:
        print_str += timed_user.user.mention + ' '
    await bot.say(print_str)


@bot.command(pass_context=True,description='Play some Dota!')
async def dota(ctx, *args):
    """Add or remove yourself from the list of waiting players.
	   Optional time parameter in minutes.
	   Optional notes.
	   e.g. !dota 60 coach or siltbreaker"""
    user = ctx.message.author
	#Remove the user and return if applicable
    if if_user_available_remove(user):
        await bot.say(user.name + ' is no longer playing (' + str(len(timed_users)) + '/5)')
        return
	
    #Set default values for time and note
    #Then check extra args to see if the user entered them
	#Assigns the first the value found in args to time if int
	#Assigns rest of the args to note
    time = None
    note = ''
    if len(args) == 0: 
        time = TIMEOUT_DEFAULT
        print('Time defaulted')
    for arg in args:
        if not time:
            try:
                time = int(arg)
                print('Time = ' + arg )
            except ValueError:
                time = TIMEOUT_DEFAULT
                note += arg + ' '
                print('Time defaulted')
        else:
            note += arg + ' '
    print('Note: ' + note)
    #Add the user to the list
    try:
        new_player = TimedUser(user, time, note)
    except Exception:
        bot.say("Wrong type for timeout minutes")
        return
    timed_users.append(new_player)
    print('User added: ' + str(user))
    await bot.say(user.name + ' is up to play Dota! (' + str(len(timed_users)) + '/5)')

    if len(timed_users) == 5:
        await alert()

			
bot.loop.create_task(check_timers())
# client.loop.create_task(print_who())
if not BOT_TOKEN:
    print('Missing Bot token!')
bot.run(BOT_TOKEN)



