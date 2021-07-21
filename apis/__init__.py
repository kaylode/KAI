from .food_api import FoodAPI
from .dictionary import Dictionary

def get_api(name):
    if name == 'dictionary':
        return Dictionary()
    if name == 'foodapi':
        return FoodAPI()