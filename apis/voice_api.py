from .base import API
from google_speech import Speech
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
        speech = Speech(text, lang)
        # speech.play()

        # # you can also apply audio effects while playing (using SoX)
        # # see http://sox.sourceforge.net/sox.html#EFFECTS for full effect documentation
        # sox_effects = ("speed", "1.5")
        # speech.play(sox_effects)

        # save the speech to an MP3 file (no effect is applied)

        filename = "output.mp3"
        speech.save(filename)

        response = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        reply = False
        return response, reply

