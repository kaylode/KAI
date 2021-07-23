from .food_api import FoodAPI
from .dictionary import Dictionary
from .translate_api import GoogleTranslationAPI
from .helper import Helper
from .voice_api import GoogleVoiceAPI
from .kaylode_api import KaylodeAPI

def get_api(name):
    if name == 'dictionary':
        return Dictionary()
    if name == 'foodapi':
        return FoodAPI()
    if name == 'translateapi':
        return GoogleTranslationAPI()
    if name == 'helper':
        return Helper()
    if name == 'voiceapi':
        return GoogleVoiceAPI()
    if name == 'kaylodeapi':
        return KaylodeAPI()