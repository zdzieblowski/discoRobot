import os
import json

import discord
from discord import DMChannel

import TenGiphPy

##

with open('config.json') as config_file:
        config_data = json.load(config_file)

version = '0.0.2'
logging = True

##

client = discord.Client()

t = TenGiphPy.Tenor(token=config_data["tenor_key"])
g = TenGiphPy.Giphy(token=config_data["giphy_key"])

##

is_ready = False

##

def get_guild_names():
        guilds = client.guilds
        list = ''
        for g in range(0, len(guilds)):
                list += '{0}'.format(guilds[g])
                if g != len(guilds)-1:
                        list += ' | '
        return '[ {0} ]'.format(list)

##

@client.event
async def on_ready():
        global is_ready
        print('Logged in as {0.user.name} on {1}\nWebSocket latency: {0.latency}s\n'.format(client, get_guild_names()))
        is_ready = True

@client.event
async def on_message(message):
        if is_ready:
                message_channel = client.get_channel(message.channel.id)
                type = ''
                content = ''
                if isinstance(message_channel, DMChannel):
                        details = '[ {0.channel} / {0.author} ]'.format(message)
                else:
                        details = '[ {0.guild} / {0.channel.name} / {0.author} / {0.author.nick} ]'.format(message)
                if message.author != client.user:
                        message_content = message.content

                        if message_content.startswith('$'):
                                type = '<CmdSuccess>'

                                command_split = message_content.split(' ');
                                command = command_split[0]
                                command_attr = command_split[1:len(command_split)];

                                aliases = {'tenor': ['$tenor', '$t'],'giphy': ['$giphy', '$g']}

                                return_message = ''

                                if command == '$help':
                                        return_message = '```DiscoRobot HELP\n\n$echo [attr] - echoes given attributes\n$giphy [attr] - shows random Giphy GIF found based on attributes given\n$tenor [attr] - shows random Tenor GIF based on attributes given```'
                                elif command == '$echo':
                                        return_message = '``ECHO: {0}``'.format(command_attr)
                                elif command in aliases['giphy']:
                                        ggif = g.random(tag = ' '.join(command_attr))['data']['images']['downsized_large']['url']
                                        return_message = '{0}'.format(ggif)
                                elif command in aliases['tenor']:
                                        tgif = t.random(' '.join(command_attr))
                                        return_message = '{0}'.format(tgif)
                                else:
                                        type = '<CmdFailure>'
                                        return_message = '``UNKNOWN COMMAND "{0}"``'.format(command)

                                await message_channel.send(return_message)

                        else:
                                type = '<Message>'
                        if logging:
                                content = ': {0}'.format(message.content)
                        print('{0} {1} {2}'.format(type,details,content))

##

print('// discoRobot v{0} [API v{1.major}.{1.minor}.{1.micro}:{1.serial} {1.releaselevel}]\n'.format(version,discord.version_info))
client.run(config_data["discord_key"])
