import discord
import asyncio
from .base import API
from utils.utils import makeEmbed
from discord_together import DiscordTogether

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

    async def get_link(self, activity):
        """
        Get invite link
        """

        link = await self.togetherControl.create_link(self.voice_channel_id, activity)
        return link

    async def do_command(self, command, trigger):
        """
        Create Discord activity link and embed it
        """

        response = None
        reply = False

        if command.startswith('setid'):
            channel_id = command.split('setid')[-1].lstrip().rstrip()
            response = "Voice channel ID is set successfully"
            self.set_voice_channel(channel_id)
        elif command.startswith('help'):
            response = "Only supports youtube, poker, betrayal, fishing, chess"
        elif command in ACTIVITIES:
            link = await self.get_link(command)
            response = makeEmbed(
                text= f"Click the blue link to start activity!\n[Invite link]({link})",
                title= f"Activity 👨‍👩‍👦",
                field_name=f"{command.capitalize()}",
                colour=discord.Colour.magenta())
        else:
            response = "Activity is not available. Use $together help"

        return response, reply
            
