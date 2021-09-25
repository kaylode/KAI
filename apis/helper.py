import discord
import json
from utils.utils import split_text_into_paragraphs, makeEmbed
from utils.pages import Pages

help_dict = {
    '$help': "Print usage guide of commands",
    '$translate': 'Translate text in double quotes. Ex: $translate "hello"',
    '$speak': 'Speak a message. Ex: $speak "hello"',
    '$voice': 'Whether to reply using voice. Ex: $voice on',
    '$ai': {
        'url': "Set ngrok server API",
        'detect': "Detect objects from image"
    },
    '$food': {
        'url': "Set ngrok server API",
        'predict': "Detect food from image"
    },
    '$gettime': 'Get system time',
    '$covid': {
        'summary': 'Get infomation of COVID in global or specific country. Ex: $covid summary'
    },

    '$openai': 'Chat with OpenAI GPT-3. Ex: $openai "mày tên gì ?"',

    "song": {
        '$play': 'Play song from Youtube. Ex: $play music',
        '$pause': 'Pause song. Ex: $pause',
        '$resume': '\Resume song. Ex: $resume',
        '$skip': 'Skip to ith song. Ex: $skip 5',
        '$next': 'Skip to next song. Ex: $next',
        '$clear': 'Clear song queue. Ex: $clear',
        '$queue': 'Show song queue. Ex: $queue',
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
                field_name='Show all commands [{page_id}' + f'/{len(result_string)}]',
                colour=discord.Colour.gold(),
                reactions=["◀️", "▶️"]
            )
        
        if trigger.startswith('$voicehelp'):
            response = stringify_dict(command, voice_dict)

            result_string = split_text_into_paragraphs(response, size=10)
                    
            pages = Pages(
                result_string,
                title='Voice Helper 💡',
                field_name='Show all voice commands [{page_id}' + f'/{len(result_string)}]',
                colour=discord.Colour.gold(),
                reactions=["◀️", "▶️"]
            )

        response = ['💗', pages]

        return response, reply