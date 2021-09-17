import discord


def makeEmbed(text, title, field_name):
    retStr = str(f"```css\n{text}```")
    embed = discord.Embed(title=title)
    embed.add_field(name=field_name, value=retStr)
    return embed