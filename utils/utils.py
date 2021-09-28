import discord
import wave
from emoji import UNICODE_EMOJI

def split_text_into_paragraphs(text, size=20):
    lines = text.split('\n')
    paragraphs = ['\n'.join(lines[i:i + size]) for i in range(0, len(lines), size)]
    return paragraphs
    
def makeEmbed(text, title=None, field_name=None, colour=discord.Colour.red()):
    retStr = str(f"```css\n{text}```")
    embed = discord.Embed(title=title, colour=colour)

    embed.add_field(name=field_name, value=retStr)
    return embed

def makeSongEmbed(field, song, colour=discord.Colour.blue()):
    embed = discord.Embed(title='Music :musical_note:', colour=colour)
    embed.add_field(name=field, value=str(f"```html\n{song.title}```"), inline=False)
    embed.set_thumbnail(url=song.thumbnail)
    embed.add_field(name="Duration 🕒", value=song.duration, inline=True)
    embed.add_field(name="View count 👀", value=song.view_count, inline=True)
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Likes count 👍", value=song.like_count, inline=True)
    embed.add_field(name="Dislikes count 👎", value=song.dislike_count, inline=True)
    return embed

def convertPCM2WAV(
    inpath='./.cache/recording.pcm', 
    outpath='./.cache/recording.wav'):
    
    with open(inpath, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
        
    with wave.open(outpath, 'wb') as wavfile:
        wavfile.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)

def is_emoji(s):
    return s in UNICODE_EMOJI['en']