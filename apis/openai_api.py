import os
import openai
from .base import API
from .translate_api import GoogleTranslationAPI

openai.api_key = os.getenv("OPENAI_API_KEY")

def find_text(text):  
    """
    Find string inside double quotes    
    """
    import re
    matches=re.findall(r'\"(.+?)\"',text)
    return matches[0]

class OpenAIAPI(API):
    """
    OpenAI API
    https://beta.openai.com/
    """
    def __init__(self) -> None:
        super().__init__()
        self.trigger = "$openai"
        self.model = openai.Completion
        self.translator = GoogleTranslationAPI()

    def get_response(self, prompt, type='chat'):
        """
        Get reponse from OpenAI GPT-3
        """
        default_prompt = ""
        if type == 'chat':
            default_prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: "

        if type == 'qa':
            default_prompt = 'I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Đéo biết\"\nQ:'

        merged_prompt = default_prompt + prompt
        response = self.model.create(
            engine="davinci",
            prompt=merged_prompt,
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )

        return response

    def do_command(self, command):
        """
        Execute command
        """
        response = None
        reply = True

        # command ex: $openai "Hello"
        try:
            text = find_text(command) # find texts in double quotes

            lang = self.translator.detect_language(text)
            en_translated = self.translator.translate(text, src=lang, dest='en')

            if text[-1] == '?':
                typed='qa'
            else:
                typed='chat'

            response = self.get_response(en_translated, type=typed)
        except Exception as e:
            response = "[Error] " + str(e)

        return response, reply