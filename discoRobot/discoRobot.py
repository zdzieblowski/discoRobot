import os
import json
import random

import discord
from discord import DMChannel

import TenGiphPy
import pyimgur

##

with open("config.json") as config_file:
        config_data = json.load(config_file)

version = "0.0.3"
logging = True

##

client = discord.Client()

g = TenGiphPy.Giphy(token = config_data["giphy_key"])
i = pyimgur.Imgur(config_data["imgur_id"])
t = TenGiphPy.Tenor(token = config_data["tenor_key"])

##

is_ready = False

##

def get_guild_names():
        guilds = client.guilds
        list = ""
        for g in range(0, len(guilds)):
                list += "{0}".format(guilds[g])
                if g != len(guilds)-1:
                        list += " | "
        return "[ {0} ]".format(list)

def imgur_search(query):
        igur_image = ""

        igur_search = i.search_gallery(query)

        if len(igur_search) > 0:
                igur_item = igur_search[random.randrange(len(igur_search))]

                if type(igur_item) is pyimgur.Gallery_image:
                        igur_image = igur_item.link
                else:
                        if len(igur_item.images) > 0:
                                igur_image = igur_item.images[random.randrange(len(igur_item.images))].link
                        else:
                                igur_image = "sorry, too rare"
        else:
                igur_image = "sorry, too rare"

        return igur_image

##

@client.event
async def on_ready():
        global is_ready
        print("Logged in as {0.user.name} on {1}\nWebSocket latency: {0.latency}s\n".format(client, get_guild_names()))
        is_ready = True

@client.event
async def on_message(message):
        if is_ready:
                message_channel = client.get_channel(message.channel.id)
                type = ""
                content = ""
                if isinstance(message_channel, DMChannel):
                        details = "[ {0.channel} / {0.author} ]".format(message)
                else:
                        details = "[ {0.guild} / {0.channel.name} / {0.author} / {0.author.nick} ]".format(message)
                if message.author != client.user:
                        message_content = message.content

                        if message_content.startswith("$"):
                                type = "<CmdSuccess>"

                                command_split = message_content.split(" ");
                                command = command_split[0]
                                command_attr = command_split[1:len(command_split)];

                                aliases = {"tenor": ["$tenor", "$t"], "giphy": ["$giphy", "$g"], "imgur": ["$imgur","$i"], "echo": ["$echo"]}

                                return_message = ""

                                if command == "$help":
                                        return_message = "> **discoRobot**\n\n*version {0}*\n\n```asciidoc\n{1} [attr] :: shows random result for `[attr]' search on Giphy\n{2} [attr] :: shows random result for `[attr]' search on Imgur\n{3} [attr] :: shows random result for `[attr]' search on Tenor```".format(version, aliases['giphy'], aliases['imgur'], aliases['tenor'])
                                elif command in aliases["echo"]:
                                        return_message = "``ECHO: {0}``".format(command_attr)
                                elif command in aliases["giphy"]:
                                        try:
                                                ggif = g.random(tag = " ".join(command_attr))["data"]["images"]["downsized_large"]["url"]
                                                return_message = "{0}".format(ggif)
                                        except:
                                                return_message = "sorry, too rare"
                                elif command in aliases["imgur"]:
                                        igur = imgur_search(" ".join(command_attr))
                                        return_message = "{0}".format(igur)
                                elif command in aliases["tenor"]:
                                        try:
                                                tgif = t.random(" ".join(command_attr))
                                                return_message = "{0}".format(tgif)
                                        except:
                                                return_message = "sorry, too rare"
                                else:
                                        type = "<CmdFailure>"
                                        return_message = "``UNKNOWN COMMAND '{0}'``".format(command)

                                await message_channel.send(return_message)

                        else:
                                type = "<Message>"
                        if logging:
                                content = ": {0}".format(message.content)
                        print('{0} {1} {2}'.format(type,details,content))

##

print("// discoRobot v{0} [API v{1.major}.{1.minor}.{1.micro}:{1.serial} {1.releaselevel}]\n".format(version,discord.version_info))
client.run(config_data["discord_key"])
