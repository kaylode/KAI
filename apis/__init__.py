from .food_api import FoodAPI
from .dictionary import Dictionary
from .translate_api import GoogleTranslationAPI

def get_api(name):
    if name == 'dictionary':
        return Dictionary()
    if name == 'foodapi':
        return FoodAPI()
    if name == 'translateapi':
        return GoogleTranslationAPI()