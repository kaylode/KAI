import asyncio
import discord
import yt_dlp
import random
import time
from utils.utils import split_text_into_paragraphs, makeEmbed, makeSongEmbed
from utils.pages import Pages

# Suppress noise about console usage from errors
# yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'flatplaylist':True,
    'geobypass':True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    """
    Load music source from Youtube query
    """
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')
        self.duration = time.strftime('%M:%S', time.gmtime(int(data.get('duration'))))
        self.view_count = '{:,}'.format(int(data.get('view_count')))
        self.like_count = '{:,}'.format(int(data.get('like_count')))
        self.dislike_count = '{:,}'.format(int(data.get('dislike_count')))

    @classmethod
    def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = ytdl.extract_info(url, download=not stream)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicAPI():
    """
    Play music from youtube
    https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
    """
    def __init__(self, client) -> None:
        self.triggers = [
            "$play", "$volume", "$voice",
            "$resume", "$continue",
            "$pause", "$stop",
            "$skip", '$next',
            "$queue", "$clear",
            "$shuffle", "$remove"]

        self.client = client

    async def do_command(self, command, trigger):
        """
        Play music
        """

        response = None

        # Example call: $play Despacito
        if trigger.startswith('$play'):
            url = command.lstrip().rstrip()
            music = self.play_from_url(url)
            if isinstance(music, str):
                response = music
            else:
                embed = makeSongEmbed('Queueing', music, colour=discord.Colour.blue())
                response = [music, embed]
        
        if self.client.voice_client is not None:

            # Example call: $pause | $stop
            if trigger.startswith('$pause') or trigger.startswith('$stop'):
                if not self.client.voice_client.is_paused():
                    self.client.voice_client.pause()
                    response = '💗'

            # Example call: $resume | $continue
            if trigger.startswith('$resume') or trigger.startswith('$continue'):
                if self.client.voice_client.is_paused():
                    self.client.voice_client.resume()
                    response = '💗'

            # Example call: $next
            if trigger.startswith('$next'):
                self.client.voice_client.stop()
                response = '💗'

            # Example call: $skip 5
            if trigger.startswith('$skip'):
                num_songs = command
                if num_songs == '':
                    num_songs = 1
                try:
                    num_songs = int(num_songs)
                    for i in range(num_songs-1):
                        self.client.voice_queue.pop(0)
                    self.client.voice_client.stop()
                    response = '💗'
                except:
                    pass

            # Example call: $clear
            if trigger.startswith('$clear'):
                while len(self.client.voice_queue) > 0:
                    self.client.voice_queue.pop(0)
                self.client.voice_client.stop()
                response = '💗'

            # Example call: $remove 5
            if trigger.startswith('$remove'):
                ith_song = command
                try:
                    ith_song = int(ith_song)
                    self.client.voice_queue.pop(ith_song-1)
                    response = '💗'
                except:
                    pass
            
            # Example call: $shuffle
            if trigger.startswith('$shuffle'):
                random.shuffle(self.client.voice_queue)
                response = '💗'

            # Example call: $queue
            if trigger.startswith('$queue'):
                
                result_string = []
                if self.client.current_song_name is not None:
                    result_string.append(f"0. {self.client.current_song_name}")
                for i, song in enumerate(self.client.voice_queue):
                    result_string.append(f"{i+1}. {song.title}")
                if len(result_string) == 0:
                    result_string = "Queue is empty"
                else:
                    result_string = '\n'.join(result_string)
                
                result_string = split_text_into_paragraphs(result_string, size=5)
                
                pages = Pages(
                    result_string,
                    title='Music :musical_note:',
                    field_name='Queue [{page_id}' + f'/{len(result_string)}]',
                    colour=discord.Colour.blue(),
                    reactions=["◀️", "▶️"]
                )
                
                response = ['💗', pages]


            # Example call: $volume 50
            if trigger.startswith('$volume'):
                # voice = get(client.voice_clients, guild=ctx.guild)  
                if command.isnumeric():
                    volume = int(command)
                    if 0 <= volume <= 100:                              
                        if self.client.voice_client.is_playing():                          
                            new_volume = volume / 100                   
                            self.client.voice_client.source.volume = new_volume
                            response = '💗'
                else:
                    if command == 'up':
                        current_volume = self.client.voice_client.source.volume
                        new_volume = min(1.0, current_volume+0.2)
                        self.client.voice_client.source.volume = new_volume
                        response = '💗'
                    if command == 'down':
                        current_volume = self.client.voice_client.source.volume
                        new_volume = max(0.0, current_volume-0.2)
                        self.client.voice_client.source.volume = new_volume
                        response = '💗'

            # Voice on/off
            if trigger.startswith('$voice'):
                type = command
                if type == 'on':
                    self.client.voice_on = True
                    embed = makeEmbed('Turn on voice reply', 'Info 🔉', 'Voice reply', colour=discord.Colour.magenta())
                    response = ['💗', embed]
                elif type == 'off':
                    self.client.voice_on = False
                    embed = makeEmbed('Turn off voice reply', 'Info 🔉', 'Voice reply', colour=discord.Colour.magenta())
                    response = ['💗', embed]

                
        return response, False

    def play_from_url(self, url):
        """
        Plays from a url (almost anything youtube_dl supports)
        """
        try:
            response = YTDLSource.from_url(url, loop=None, stream=True)
        except:
            response = "Không tìm thấy bài hát"
        
        return response