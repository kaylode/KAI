import os
from .base import API
from gtts import gTTS
from googletrans import Translator

import discord

CACHE_DIR ='./.cache'

def find_text(text):  
    """
    Find string inside double quotes    
    """
    import re
    matches=re.findall(r'\"(.+?)\"',text)
    return matches[0]

class GoogleVoiceAPI(API):
    """
    Google Text-To-Speech API
    https://github.com/pndurette/gTTS
    """
    translator = Translator()
    def __init__(self) -> None:
        super().__init__()
        self.triggers = ["$speak"]

    @staticmethod
    def speak(text, lang=None):
        """
        Convert text to speech, save to mp3 and convert to Discord player
        """
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        filename = os.path.join(CACHE_DIR, "temp.mp3")

        if lang is None:
            # Detect language
            lang = GoogleVoiceAPI.translator.detect(text).lang

        # Saving the converted audio in a mp3 file
        speech = gTTS(text=text, lang=lang, slow=False)

        # Save to cache folder
        speech.save(filename)

        # Convert to Discord's audio file
        try:
            response = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        except Exception as e:
            response = "[Error] " + str(e)

        return response

    def do_command(self, command):
        """
        Execute command
        """
        reply = False
        text = find_text(command) # find texts in double quotes
        response = self.speak(text)   
        return response, reply

    

