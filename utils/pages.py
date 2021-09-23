import discord
from utils.utils import makeEmbed

class Pages:
    """
    Pagination class for multiple embeds
    """
    def __init__(self, list_of_contents: list[str], title: str, field_name: str, colour: int) -> None:
        self.list_of_contents = list_of_contents
        self.title = title
        self.field_name = field_name
        self.colour = colour
        self.num_pages = len(self.list_of_embeds)
        self.current_page = 1
        self.id = None

    def make_page(self):
        content = self.list_of_contents[self.current_page]
        field_name = self.field_name.format(self.current_page)
        embed = makeEmbed(
            text = content,
            title=self.title,
            field_name=field_name,
            colour=self.colour)

        return embed

    async def send_page(self, channel):
        embed = self.make_page()
        message = await channel.send(embed=embed)
        self.id = message.id
        return message