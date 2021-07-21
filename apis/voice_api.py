from .base import API
from gtts import gTTS

import discord

class GoogleVoiceAPI(API):
    """
    Google Voice API
    https://github.com/desbma/GoogleSpeech
    """
    def __init__(self) -> None:
        super().__init__()
        self.trigger = "$speak"

    def do_command(self, command):
        text = "Hello World"
        lang = "en"
  
        filename = "output.mp3"
        
        # Saving the converted audio in a mp3 file
        speech = gTTS(text=text, lang=lang, slow=False)
        speech.save(filename)

        response = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        reply = False
        return response, reply

