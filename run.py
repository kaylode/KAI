"""
Discord Docs
https://github.com/Rapptz/discord.py/tree/v1.7.3/examples
"""

import os
import discord
import random
from discord.ext import commands, tasks

# from replit import db
from server import keep_alive
from bot import KAI
from configs import get_config
from apis import GoogleVoiceAPI, Alarm
from utils.utils import makeEmbed
from utils.pages import Pages

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
        self.current_song_name = None 

        # Pages
        self.pages = []
        
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
                print(chr(27) + "[2J") # Clear console logs at specific time

    @tasks.loop(seconds=10) # task runs every 60 seconds
    async def audio_async(self):
        if self.voice_client is None or self.voice_client.is_playing():
            pass            
        else:
            if len(self.voice_queue) > 0 :
                if not self.voice_client.is_paused():
                    response = self.voice_queue.pop(0)
                    async with self.ctx.typing():
                        self.voice_client.play(response, after=lambda e: print('Player error: %s' % e) if e else None)

                    try:
                        self.current_song_name = response.title
                        embed = makeEmbed(response.title, 'Music :musical_note:', 'Now Playing :arrow_forward:', colour=discord.Colour.blue())
                        if self.prev_message is not None:
                            await self.prev_message.delete()
                        self.prev_message = await self.on_embed_response(self.ctx.channel, embed)
                    except:
                        pass
                    
                    self.voice_counter = 0
                else:
                    self.voice_counter += 10
            else:
                self.current_song_name = None 
                self.voice_counter += 10

    @audio_async.before_loop
    @time_check_async.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

    async def join_voice_channel(self, voice_state):
        """
        Joining a voice channel
        """
        # Get the channel of author
        if voice_state is not None:
            voice_channel = voice_state.channel 

            # If hasn't joined, join voice channel
            voice = discord.utils.get(client.voice_clients, guild=self.ctx.guild)
            if voice is None:
                await voice_channel.connect()
                self.voice_client = self.ctx.voice_client

    async def on_string_response(self, channel, response, reply=False, voice_state=None):
        """
        If reponse is string. Reply it by text or voice
        """

        if self.voice_on and reply:
            # If voice on, speak it
            response_voice = GoogleVoiceAPI.speak(text=response, lang='vi')
            await self.on_voice_response(response_voice, voice_state, channel)
        else:
            # Else send text
            return await channel.send(response)
    
    async def on_embed_response(self, channel, response, reactions=None):
        """
        If response is an embed. Embed it
        """
        if reactions is None:
            return await channel.send(embed=response)
        else:
            message = await channel.send(embed=response)
            for reaction in reactions:
                await message.add_reaction(reaction)

    async def on_voice_response(self, response, voice_state=None, channel=None):
        """
        If response is voice. Check voice channel connection then initialize voice queue
        """
        if not self.audio_async.is_running():
            self.audio_async.start()
    
        await self.join_voice_channel(voice_state)

        self.voice_queue.append(response)
        try:
            response = makeEmbed(response.title, 'Music :musical_note:', 'Queueing', colour=discord.Colour.blue())
            await self.on_embed_response(channel, response)
        except:
            pass
        
    async def on_file_response(self, channel, response):
        """
        If response is file. Send file
        """
        await channel.send(file=response)

    async def on_response(self, response, message, voice_state, reply):
        if isinstance(response, discord.File):
            # Image file
            await self.on_file_response(message.channel, response)
            await message.add_reaction('💗')

        if isinstance(response, discord.PCMVolumeTransformer):
            await self.on_voice_response(response, voice_state, message.channel)
            await message.add_reaction('💗')
            
        if isinstance(response, str):
            await self.on_string_response(message.channel, response, reply, voice_state)

        if isinstance(response, discord.Embed):
            self.prev_message = await self.on_embed_response(message.channel, response)

        if isinstance(response, Pages):
            message = await response.send_page(message.channel)



    # async def on_reaction_add(self, reaction, user):
    #     for page in self.pages:
    #         if reaction.message.id:
    #             pass
            
    #     if reaction.emoji == "🏃":
    #         Role = discord.utils.get(user.server.roles, name="YOUR_ROLE_NAME_HERE")
    #         await client.add_roles(user, Role)

    async def on_message(self, message):
        if message.author == client.user:
            return

        
        self.ctx = await client.get_context(message)
        voice_state = self.ctx.message.author.voice 

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
            if isinstance(response, list):
                for r in response:
                    await self.on_response(r, message, voice_state, reply)
            else:
                await self.on_response(response, message, voice_state, reply)


        if self.voice_counter > 300: 
            self.voice_counter = 0
            await self.voice_client.disconnect()
            self.voice_client = None
            if self.audio_async.is_running():
                self.audio_async.stop()

            embed = makeEmbed("Disconnected due to inactivity over 5 minutes", field_name='Disconnected', colour=discord.Colour.red())
            if self.prev_message is not None:
                await self.prev_message.delete()
            self.prev_message = await message.channel.send(embed=embed)

        if message.content.startswith('$pause') or message.content.startswith('$stop'):
            if not self.voice_client.is_paused():
                self.voice_client.pause()
                await message.add_reaction('💗')
        if message.content.startswith('$resume') or message.content.startswith('$continue'):
            if self.voice_client.is_paused():
                self.voice_client.resume()
                await message.add_reaction('💗')
        if message.content.startswith('$next'):
            self.voice_client.stop()
            await message.add_reaction('💗')
        if message.content.startswith('$skip'):
            num_songs = message.content.split('$skip')[-1].lstrip().rstrip()
            if num_songs.isspace():
                num_songs = 1
            try:
                num_songs = int(num_songs)
                for i in range(num_songs-1):
                    self.voice_queue.pop(0)
                self.voice_client.stop()
                await message.add_reaction('💗')
            except:
                pass
        if message.content.startswith('$clear'):
            while len(self.voice_queue) > 0:
                self.voice_queue.pop(0)
            self.voice_client.stop()
            await message.add_reaction('💗')

        
        if message.content.startswith('$remove'):
            ith_song = message.content.split('$remove')[-1].lstrip().rstrip()
            try:
                ith_song = int(ith_song)
                self.voice_queue.pop(ith_song-1)
                await message.add_reaction('💗')
            except:
                pass

        if message.content.startswith('$queue'):
            await message.add_reaction('💗')
            result_string = []
            if self.current_song_name is not None:
                result_string.append(f"0. {self.current_song_name}")
            for i, song in enumerate(self.voice_queue):
                result_string.append(f"{i+1}. {song.title}")
                if i == 5:
                    break
            if len(result_string) == 0:
                result_string = "Queue is empty"
            else:
                result_string = '\n'.join(result_string)
            
            embed = makeEmbed(result_string, 'Music :musical_note:', field_name='Queue', colour=discord.Colour.blue())
            if self.prev_message is not None:
                await self.prev_message.delete()
                self.prev_message = None
            await message.channel.send(embed=embed)

        if message.content.startswith('$shuffle'):
            await message.add_reaction('💗')
            random.shuffle(self.voice_queue)


            


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