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
from utils.utils import makeEmbed, is_emoji, makeSongEmbed
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
        self.bot = KAI(self.config, client=self)
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
                        embed = makeSongEmbed('Now Playing :arrow_forward:', response, colour=discord.Colour.blue())
                       
                        if self.prev_message is not None:
                            await self.prev_message.delete()
                        self.prev_message = await self.on_embed_response(self.ctx.channel, embed)
                    except:
                        pass
                    
                    self.voice_counter = 0
                else:
                    self.voice_counter += 10
                    if self.voice_counter > 300:
                        await self.leave_voice_channel_on_timeout()
            else:
                self.current_song_name = None 
                self.voice_counter += 10

                if self.voice_counter > 300:
                    await self.leave_voice_channel_on_timeout()
                    

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

    async def leave_voice_channel(self):
        """
        Leave channel on timeout
        """
        self.pages = []
        self.voice_counter = 0
        self.voice_queue = []
        self.current_song_name = None 

        if self.audio_async.is_running():
            self.audio_async.stop()

        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None

    async def leave_voice_channel_on_timeout(self):
        """
        Leave channel on timeout
        """
        await self.leave_voice_channel()
        embed = makeEmbed("Disconnected due to inactivity over 5 minutes", title="Disconnected", field_name='Timeout', colour=discord.Colour.red())
        self.prev_message = await self.on_embed_response(self.ctx.channel, embed)

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
        
    async def on_file_response(self, channel, response):
        """
        If response is file. Send file
        """
        await channel.send(file=response)

    async def on_page_response(self, channel, response):
        """
        If response is page. Send page
        """
        self.pages.append(response)
        message = await response.send_page(channel)
        return message
        
    async def on_response(self, response, message, voice_state, reply):
        """
        Deal with every kinds of response
        """
        if isinstance(response, discord.File):
            # Image file
            await self.on_file_response(message.channel, response)
            await message.add_reaction('💗')

        if isinstance(response, discord.PCMVolumeTransformer):
            await self.on_voice_response(response, voice_state, message.channel)
            await message.add_reaction('💗')
        
        if is_emoji(response):
            await message.add_reaction(response)

        elif isinstance(response, str):
            await self.on_string_response(message.channel, response, reply, voice_state)

        if isinstance(response, discord.Embed):
            if self.prev_message is not None:
                await self.prev_message.delete()
            self.prev_message = await self.on_embed_response(message.channel, response)

        if isinstance(response, Pages):
            await self.on_page_response(message.channel, response)

    async def on_reaction_add(self, reaction, user):
        """
        On reaction add to page
        """
        for page in self.pages:
            if reaction.message.id == page.id:
                if str(reaction.emoji) == page.prev_btn:
                    await page.previous_page(reaction.message)
                    await reaction.message.remove_reaction(reaction.emoji, user)
                    break
                if str(reaction.emoji) == page.next_btn:
                    await page.next_page(reaction.message)
                    await reaction.message.remove_reaction(reaction.emoji, user)
                    break

    async def on_message(self, message):
        if message.author == client.user:
            return

        self.ctx = await client.get_context(message)
        voice_state = self.ctx.message.author.voice 

        # Process message and get response 
        response, reply = await self.bot.response(message)

        # Deal with response
        if response is not None:
            if isinstance(response, list):
                for r in response:
                    await self.on_response(r, message, voice_state, reply)
            else:
                await self.on_response(response, message, voice_state, reply)

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