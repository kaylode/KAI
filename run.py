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
from apis import GoogleVoiceAPI, Alarm, SpeechToTextAPI, MusicAPI
from utils.utils import makeEmbed, convertPCM2WAV

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

        # Voice queue
        self.voice_counter = 0
        self.voice_client = None
        self.voice_queue = []
        self.prev_message = None
        
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

    # @tasks.loop(seconds=5) # task runs every x seconds
    # async def speech_check_async(self):
    #     if os.path.exists('./.cache/recording.pcm'):
    #         if os.path.exists('./.cache/recording.wav'):
    #             text = SpeechToTextAPI.speak(lang='en-US')
    #             print(text)
    #             if text is not None:
    #                 channel = self.get_channel(TEST_CHANNEL_ID)
    #                 await channel.send(text)
    #                 # response_voice = GoogleVoiceAPI.speak(text=text, lang='vi')
    #                 # self.voice_client.play(response_voice, after=lambda e: print('Player error: %s' % e) if e else None)
    #             os.remove('./.cache/recording.pcm')
    #             os.remove('./.cache/recording.wav')
    #         else:
    #             convertPCM2WAV()
    
    @tasks.loop(seconds=10) # task runs every 60 seconds
    async def audio_async(self):
        if self.voice_client is None or self.voice_client.is_playing():
            pass            
        else:
            if len(self.voice_queue) > 0:
                response = self.voice_queue.pop(0)
                async with self.ctx.typing():
                    self.voice_client.play(response, after=lambda e: print('Player error: %s' % e) if e else None)

                try:
                    embed = makeEmbed(response.title, 'Music :musical_note:', 'Now Playing :arrow_forward:')
                    self.prev_message = await self.ctx.send(embed=embed)
                except:
                    pass
                
                self.voice_counter = 0
            else:
                self.voice_counter += 10

    # @speech_check_async.before_loop
    @audio_async.before_loop
    @time_check_async.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

    async def on_message(self, message):

        self.ctx = await client.get_context(message)

        # Whether author connect to voice channel
        voice_state = self.ctx.message.author.voice 

        # Get the channel of author
        if voice_state is not None:
            voice_channel = voice_state.channel 
        else:
            voice_channel = None


        if message.author == client.user:
            if message.content.startswith('$play'):
                pass
            else:     
                return


        # Process message and get response 
        response, reply = self.bot.response(message)


        if message.content.startswith('$listen'):
            self.voice_client =  await voice_channel.connect()
            # if not self.speech_check_async.is_running():
            #     self.speech_check_async.start()
            

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
                if not self.audio_async.is_running():
                    self.audio_async.start()
                
                voice = discord.utils.get(client.voice_clients, guild=self.ctx.guild)
                if voice is None: # If hasn't joined, join voice channel
                    await voice_channel.connect()
                self.voice_client = self.ctx.voice_client

                self.voice_queue.append(response)
                try:
                    embed = makeEmbed(response.title, 'Music :musical_note:', 'Queueing')
                    self.prev_message = await message.channel.send(embed=embed)
                except:
                    pass
                await message.add_reaction('💗')
              
            else:
                # Send message
                if self.voice_on and reply:
                    if voice_state is not None: # Check if author is in voice channel
                        voice = discord.utils.get(client.voice_clients, guild=self.ctx.guild)
                        if voice is None: # If hasn't joined, join voice channel
                            await voice_channel.connect()
                            
                        response_voice = GoogleVoiceAPI.speak(text=response, lang='vi')
                        self.ctx.voice_client.play(response_voice, after=lambda e: print('Player error: %s' % e) if e else None)
                    
                await message.channel.send(response)

        if self.voice_counter > 300: 
            self.voice_counter = 0
            await self.voice_client.disconnect()
            self.voice_client = None
            if self.audio_async.is_running():
                self.audio_async.stop()

            if self.speech_check_async.is_running():
                self.speech_check_async.stop()

            embed = makeEmbed("Disconnected due to inactivity over 5 minutes", field_name='Disconnected')
            self.prev_message = await message.channel.send(embed=embed)

        if message.content.startswith('$pause'):
            if not self.voice_client.is_paused():
                self.voice_client.pause()
                await message.add_reaction('💗')
        if message.content.startswith('$resume'):
            if self.voice_client.is_paused():
                self.voice_client.resume()
                await message.add_reaction('💗')
        if message.content.startswith('$skip'):
            self.voice_client.stop()
            await message.add_reaction('💗')


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