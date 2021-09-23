import discord
import asyncio
from utils.utils import makeEmbed

reaction_map = {
    'PREV': "◀️",
    'NEXT': "▶️",
}

class Pages:
    """
    Pagination class for multiple embeds
    """
    def __init__(self, list_of_contents, title, field_name, colour, reactions=None) -> None:
        self.list_of_contents = list_of_contents
        self.title = title
        self.field_name = field_name
        self.colour = colour
        self.num_pages = len(self.list_of_contents)
        self.current_page = 1
        self.reactions = reactions
        self.id = None

        self.prev_btn = reaction_map['PREV']
        self.next_btn = reaction_map['NEXT']

    def make_page(self):
        """
        Embed the current page
        """
        content = self.list_of_contents[self.current_page-1]
        dict = {
            'page_id': self.current_page
        }
        field_name = self.field_name.format(**dict)
        embed = makeEmbed(
            text = content,
            title=self.title,
            field_name=field_name,
            colour=self.colour)

        return embed

    async def send_page(self, channel):
        """
        Send current page to channel
        """
        embed = self.make_page()

        message = await channel.send(embed=embed)

        if self.reactions is not None:
            for reaction in self.reactions:
                await message.add_reaction(reaction)
        
        await asyncio.sleep(1) # wait for on_reaction first
        self.id = message.id
        return message

    async def next_page(self, message):
        """
        Send next page to channel
        """

        if self.current_page == self.num_pages:
            return
        else:
            self.current_page += 1
            embed = self.make_page()
            message = await message.edit(embed=embed)
            return message

    async def previous_page(self, message):
        """
        Send previous page to channel
        """
        if self.current_page == 1:
            return
        else:
            self.current_page -= 1
            embed = self.make_page()
            message = await message.edit(embed=embed)
            return message