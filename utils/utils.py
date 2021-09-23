import discord
import wave

def split_text_into_paragraphs(text, size=20):
    lines = text.split('\n')
    paragraphs = ['\n'.join(lines[i:i + size]) for i in range(0, len(lines), size)]
    return paragraphs
    
def makeEmbed(text, title=None, field_name=None, colour=discord.Colour.red()):
    retStr = str(f"```css\n{text}```")
    embed = discord.Embed(title=title, colour=colour)

    embed.add_field(name=field_name, value=retStr)
    return embed

def convertPCM2WAV(
    inpath='./.cache/recording.pcm', 
    outpath='./.cache/recording.wav'):
    
    with open(inpath, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
        
    with wave.open(outpath, 'wb') as wavfile:
        wavfile.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)