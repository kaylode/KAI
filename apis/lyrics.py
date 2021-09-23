import os
import types
import discord
from .base import API
from utils.utils import makeEmbed, split_text_into_paragraphs
from utils.pages import Pages
from lyrics_extractor import SongLyrics

GCS_API_KEY = os.getenv('GCS_API_KEY')
GCS_ENGINE_ID = os.getenv('GCS_ENGINE_ID')

# Initialize Vietnamese Lyrics
def lyricsvn_scraper(self):
    extract = self.source_code.select(".detail")
    if not extract:
        return None

    lyrics = (extract[0].get_text()).replace('<br>', '\n').strip()
    return lyrics

def loibaihatbiz_scraper(self):
    extract = self.source_code.select(".lyric-song")
    if not extract:
        return None

    lyrics = (extract[0].get_text()).replace('<br>', '\n').strip()
    return lyrics

def make_pages_embed(paragraphs, title):
    embeds = []
    for i, paragraph in enumerate(paragraphs):
        embed = makeEmbed(paragraph, 'Lyric :musical_score:', f'Page {i+1}/{len(paragraphs)}', colour=discord.Colour.orange())
        embeds.append(embed)

    return embeds

# Assign new crawl method to library class
SongLyrics.scraper_factory.lyricsvn_scraper = lyricsvn_scraper
SongLyrics.scraper_factory.loibaihatbiz_scraper = loibaihatbiz_scraper

SongLyrics.SCRAPERS['lyrics.vn'] = SongLyrics.scraper_factory.lyricsvn_scraper
SongLyrics.SCRAPERS['loibaihat.biz'] = SongLyrics.scraper_factory.loibaihatbiz_scraper



class LyricsAPI(API):
    """
    Lyric API 
    https://github.com/Techcatchers/PyLyrics-Extractor    
    """
    def __init__(self) -> None:
        super().__init__()
        self.trigger = '$lyric'

        self.songlyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)
        self.songlyrics.scraper_factory.lyricsvn_scraper = types.MethodType(lyricsvn_scraper, self.songlyrics.scraper_factory) 
        self.songlyrics.scraper_factory.loibaihatbiz_scraper = types.MethodType(loibaihatbiz_scraper, self.songlyrics.scraper_factory) 
        SongLyrics.SCRAPERS['lyrics.vn'] = SongLyrics.scraper_factory.lyricsvn_scraper
        SongLyrics.SCRAPERS['loibaihat.biz'] = SongLyrics.scraper_factory.loibaihatbiz_scraper

        self.reactions = ["◀️", "▶️"]

    def do_command(self, command):
        """
        Get lyrics of the song
        """
        crawled = self.songlyrics.get_lyrics(command)
        lyrics = crawled['lyrics']
        title = crawled['title']
        paragraphs = split_text_into_paragraphs(lyrics)
        try:
            response = Pages(
                paragraphs, 
                title='Lyric :musical_score:', 
                field_name= "Page {page_id}" + f'/{len(paragraphs)}: {title}', 
                colour=discord.Colour.orange(),
                reactions=self.reactions)
            # response = make_pages_embed(paragraphs, title)
        except:
            response = "Lyric not found"
        reply = True
        return response, reply