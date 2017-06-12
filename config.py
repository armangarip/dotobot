import configparser
import os.path
import sys

f = sys.path[0] + '\\config.ini'

def createConfig(config):
    config['BOT'] = {'Token': ''}
    config['CHANNELS'] = {'DotaChannelID': '',
                          'BotChannelID': ''}
    config['DEFAULT_VALUES'] = {'timeout': '60',
                                'alertText': 'go'}
    with open(f, 'w+') as configfile:
        config.write(configfile)
								
def readConfig(config):
    config.read(f)

def getConfig():
    config = configparser.ConfigParser()		
    if not os.path.isfile(f):
        createConfig(config)
    readConfig(config)
    return config