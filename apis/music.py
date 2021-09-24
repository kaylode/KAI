import asyncio
import discord
import youtube_dl

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    """
    Load music source from Youtube query
    """
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

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
            "$play", 
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

        # Example call: $play Despacito

        if trigger.startswith('play'):
            url = command.lstrip().rstrip()
            response = self.play_from_url(url)
        
        if trigger.startswith('$pause') or trigger.startswith('$stop'):
            if not self.client.voice_client.is_paused():
                self.client.voice_client.pause()
                
        return response, False

    @staticmethod
    def play_from_url(url):
        """
        Plays from a url (almost anything youtube_dl supports)
        """
        try:
            response = YTDLSource.from_url(url, loop=None, stream=True)
        except:
            response = "Không tìm thấy bài hát"
        
        return response