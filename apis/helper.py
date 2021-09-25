import discord
import json
from utils.utils import split_text_into_paragraphs, makeEmbed
from utils.pages import Pages

help_dict = {
    '$help': "\t\t\t\t Print usage guide of commands",
    '$translate': '\t\t\tTranslate text in double quotes. Ex: $translate "hello"',
    '$speak': '\t\t\t\tSpeak a message. Ex: $speak "hello"',
    '$voice': '\t\t\t\tWhether to reply using voice. Ex: $voice on',
    '$ai': {
        'url': "\t\t\t\tSet ngrok server API",
        'detect': "\t\t\tDetect objects from image"
    },
    '$food': {
        'url': "\t\t\t\tSet ngrok server API",
        'predict': "\t\t\tDetect food from image"
    },
    '$gettime': '\t\t\tGet system time',
    '$covid': {
        'summary': '\t\t\tGet infomation of COVID in global or specific country. Ex: $covid summary'
    },

    '$openai': '\t\t\tChat with OpenAI GPT-3. Ex: $openai "mày tên gì ?"',

    "song": {
        '$play': '\t\t\tPlay song from Youtube. Ex: $play music',
        '$pause': '\t\t\tPause song. Ex: $pause',
        '$resume': '\t\t\Resume song. Ex: $resume',
        '$skip': '\t\t\tSkip to ith song. Ex: $skip 5',
        '$next': '\t\t\tSkip to next song. Ex: $next',
        '$clear': '\t\t\tClear song queue. Ex: $clear',
        '$queue': '\t\t\tShow song queue. Ex: $queue',
    }
}

with open('./database/db.json', 'r') as f:
    voice_dict = json.load(f)
    voice_dict = voice_dict['voice']


def stringify_dict(command, _dict):
    response = ""
    for key in _dict.keys():
        command = command.rstrip().lstrip()
        if command == key or command == "":
            response += f"{key}: "
            details = _dict[key] # Dict or string
            if isinstance(details, dict):
                response += "\n"
                for key2, value in details.items():
                    response += f"\t{key2}: {value}\n"
            else:
                response += f"{details}\n"
    return response

class Helper:
    """
    Helper class for printing BOT information
    """
    def __init__(self) -> None:
        self.triggers = ["$help", "$voicehelp"]

    def do_command(self, command, trigger):
        """
        Execute command
        """
        reply = False

        if trigger.startswith('$help'):
            response = stringify_dict(command, help_dict)

            result_string = split_text_into_paragraphs(response, size=10)
                    
            pages = Pages(
                result_string,
                title='Helper 💡',
                field_name='Show all commands',
                colour=discord.Colour.gold(),
                reactions=["◀️", "▶️"]
            )
        
        if trigger.startswith('$voicehelp'):
            response = stringify_dict(command, voice_dict)

            result_string = split_text_into_paragraphs(response, size=10)
                    
            pages = Pages(
                result_string,
                title='Voice Helper 💡',
                field_name='Show all voice commands',
                colour=discord.Colour.gold(),
                reactions=["◀️", "▶️"]
            )
        
        response = ['💗', pages]

        return response, reply