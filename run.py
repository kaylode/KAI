"""
Discord Docs
https://github.com/Rapptz/discord.py/tree/v1.7.3/examples
"""

import os
import discord
from discord.ext import commands, tasks

# from replit import db
from server import keep_alive
from bot import KAI
from configs import get_config
from apis import GoogleVoiceAPI, Alarm

TEST_CHANNEL_ID = 865577241048383492
ASTROMENZ_CHANNEL_ID = 760897275890368525

class MyClient(commands.Bot):
    """
    Custom Client
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # KAI initilization
        self.config = get_config("KAI")
        self.bot = KAI(self.config)
        self.ctx = None
        self.voice_on = False
        
        # Alarm
        self.alarm = Alarm()
        self.channel_ids = [TEST_CHANNEL_ID, ASTROMENZ_CHANNEL_ID] # need to be list for all text channels

        # create the background task and run it in the background
        self.time_check_async.start()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    @tasks.loop(seconds=Alarm.loop_second) # task runs every x seconds
    async def time_check_async(self):
        for channel_id in self.channel_ids:
            channel = self.get_channel(channel_id) # channel ID goes here
            response = self.alarm.time_check()
            if channel is not None and response is not None:
                await channel.send(response)

    @time_check_async.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

    async def on_message(self, message):

        if message.author == client.user:
            return

        self.ctx = await client.get_context(message)

        # Whether author connect to voice channel
        voice_state = self.ctx.author.voice 

        # Get the channel of author
        if voice_state is not None:
            voice_channel = voice_state.channel 
        else:
            voice_channel = None

        # Process message and get response 
        response, reply = self.bot.response(message)

        # Voice on/off
        if message.content.startswith('$voice'):
            type = message.content.split('$voice')[-1].lstrip().rstrip()
            if type == 'on':
                self.voice_on = True
                response = '[Info] Voice reply on'
            elif type == 'off':
                self.voice_on = False
                response = '[Info] Voice reply off'
            else:
                response = '[Error] Wrong command. Use $voice on/off only'

        # Deal with response
        if response is not None:
            if isinstance(response, discord.File):
                # Image file
                await message.channel.send(file=response)
            elif isinstance(response, discord.PCMVolumeTransformer):
                voice = discord.utils.get(client.voice_clients, guild=self.ctx.guild)
                if voice is None: # If hasn't joined, join voice channel
                    await voice_channel.connect()
                self.ctx.voice_client.play(response, after=lambda e: print('Player error: %s' % e) if e else None)
            else:
                # Send message
                if self.voice_on and reply:
                    if voice_state is not None: # Check if author is in voice channel
                        voice = discord.utils.get(client.voice_clients, guild=self.ctx.guild)
                        if voice is None: # If hasn't joined, join voice channel
                            await voice_channel.connect()
                        response = GoogleVoiceAPI.speak(text=response, lang='vi')
                        self.ctx.voice_client.play(response, after=lambda e: print('Player error: %s' % e) if e else None)
                    else:
                        await message.channel.send(response)
                else:
                    await message.channel.send(response)

        # self.bot.set_database(message, db)

# Create new processes to keep server online
keep_alive()

# Get user token
TOKEN = os.getenv('TOKEN')

# Discord client
client = MyClient(
    command_prefix='$', 
    intents=discord.Intents.default())

# Start client
client.run(TOKEN)