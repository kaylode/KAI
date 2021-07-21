from .base import API
from googletrans import Translator

def find_text(text):      
  import re
  matches=re.findall(r'\"(.+?)\"',text)
  return ",".join(matches)

class GoogleTranslationAPI(API):
    def __init__(self) -> None:
        super().__init__()
        self.trigger = "$translate"
        self.translator = Translator()

    def do_command(self, command):
        response = None
        reply = False

        # command ex: $translate "Hello"
        text = find_text(command) # find texts in double quotes
        result = self.translator.translate(text, dest='vi')
        response = result.text


        return response, reply
        