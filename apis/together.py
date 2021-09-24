import discord
import asyncio
from .base import API
from utils.utils import makeEmbed
from discordTogether import DiscordTogether

ACTIVITIES = ("youtube","poker","betrayal","fishing","chess")

class DicordTogetherAPI(API):
    """
    Discord Together API for creating Activity
    https://github.com/apurv-r/discord-together
    """
    def __init__(self, client) -> None:
        super().__init__()
        self.triggers = ["$together"]
        self.togetherControl = DiscordTogether(client)
        self.voice_channel_id = None

    def set_voice_channel(self, channel_id):
        self.voice_channel_id = channel_id

    def get_link(self, activity):
        """
        Get invite link
        """

        loop = asyncio.get_event_loop()
        link = loop.run_until_complete(self.togetherControl.create_link(self.voice_channel_id, activity))
        
        return link

    def do_command(self, command):
        """
        Create Discord activity link and embed it
        """

        response = None
        reply = False

        if command in ACTIVITIES:
            if command == 'help':
                response = "Only supports youtube, poker, betrayal, fishing, chess"
            else:
                link = self.get_link(command)
                response = makeEmbed(
                    text= f"Click the blue link to start activity!\n{link}",
                    title= f"Activity 👨‍👩‍👦",
                    field_name=f"{command.capitalize()}",
                    colour=discord.Colour.yellow())
        else:
            response = "Activity is not available. Use $together help"

        return response, reply
            