from .base import API
from googletrans import Translator

def find_text(text):  
    """
    Find string inside double quotes    
    """
    import re
    matches=re.findall(r'\"(.+?)\"',text)
    return matches[0]

class GoogleTranslationAPI(API):
    """
    Google translation API
    https://py-googletrans.readthedocs.io/en/latest/
    """
    def __init__(self) -> None:
        super().__init__()
        self.trigger = "$translate"
        self.translator = Translator()

    def do_command(self, command):
        """
        Execute command
        """
        response = None
        reply = False

        # command ex: $translate "Hello"
        try:
            text = find_text(command) # find texts in double quotes
            response = self.translate(text)
            return response, reply
        except Exception as e:
            response = "[Error] " + str(e)

        return response, reply

    def detect_language(self, text):
        """
        Detect text's language
        """
        result = self.translator.detect(text)
        lang = result.lang
        return lang

    def translate(self, text, src=None, dest='vi'):
        """
        Translate a text
        """
        if src is None:
            src = self.detect_language(text)

        result = self.translator.translate(text,src=src, dest=dest)
        response = result.text
        return response
        