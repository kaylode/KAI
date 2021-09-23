import os
import types
from .base import API
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

def split_text_into_paragraphs(text, size=10):
    lines = text.split('\n')
    paragraphs = ['\n'.join(lines[i:i + size]) for i in range(0, len(lines), size)]
    return paragraphs


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

    def do_command(self, command):
        """
        Get lyrics of the song
        """
        try:
            response = self.songlyrics.get_lyrics(command)['lyrics']
            response = split_text_into_paragraphs(response)
        except:
            response = "Lyric not found"
        reply = True
        return response, reply


