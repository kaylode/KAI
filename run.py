"""
Discord Docs
https://github.com/Rapptz/discord.py/tree/v1.7.3/examples
"""

import os
import discord
from discord.ext import commands

from replit import db
from server import keep_alive
from bot import KAI
from configs import get_config
from apis import GoogleVoiceAPI

# Discord client
description = '''
An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.
'''
intents = discord.Intents.default()
client = commands.Bot(command_prefix='$', description=description, intents=intents)

# KAI initilization
config = get_config("KAI")
bot = KAI(config)
ctx = None
voice_on = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global voice_on
    global ctx

    if message.author == client.user:
        return

    ctx = await client.get_context(message)

    # Whether author connect to voice channel
    voice_state = ctx.author.voice 

    # Get the channel of author
    if voice_state is not None:
        voice_channel = voice_state.channel 
    else:
        voice_channel = None

    # Process message and get response 
    response, reply = bot.response(message)

    # Voice on/off
    if message.content.startswith('$voice'):
        type = message.content.split('$voice')[-1].lstrip().rstrip()
        if type == 'on':
            voice_on = True
            response = '[Info] Voice reply on'
        elif type == 'off':
            voice_on = False
            response = '[Info] Voice reply off'
        else:
            response = '[Error] Wrong command. Use $voice on/off only'

    # Deal with response
    if response is not None:
        if isinstance(response, discord.File):
            # Image file
            await message.channel.send(file=response)
        elif isinstance(response, discord.PCMVolumeTransformer):
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            if voice is None: # If hasn't joined, join voice channel
                await voice_channel.connect()
            ctx.voice_client.play(response, after=lambda e: print('Player error: %s' % e) if e else None)
        else:
            # Send message
            if voice_on and reply:
                if voice_state is not None: # Check if author is in voice channel
                    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                    if voice is None: # If hasn't joined, join voice channel
                        await voice_channel.connect()
                    response = GoogleVoiceAPI.speak(text=response, lang='vi')
                    ctx.voice_client.play(response, after=lambda e: print('Player error: %s' % e) if e else None)
                else:
                    await message.channel.send(response)
            else:
                await message.channel.send(response)

        # bot.set_database(message, db)

# Create new processes to keep server online
keep_alive()

# Get user token
TOKEN = os.getenv('TOKEN')

# Start client
client.run(TOKEN)