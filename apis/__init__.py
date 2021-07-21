from .food_api import FoodAPI
from .dictionary import Dictionary
from .translate_api import GoogleTranslationAPI
from .helper import Helper

def get_api(name):
    if name == 'dictionary':
        return Dictionary()
    if name == 'foodapi':
        return FoodAPI()
    if name == 'translateapi':
        return GoogleTranslationAPI()
    if name == 'helper':
        return Helper()