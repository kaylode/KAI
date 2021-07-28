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
        self.type = "chat"
        self.current_prompt = {
            'chat': "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.",
            'qa': 'I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with "Đéo biết"'
        }
        self.translator = GoogleTranslationAPI()

    def set_message_type(self, type):
        if type in self.current_prompt.keys():
            self.type = type
            response = f"[Info] Set OpenAI type to {type}"
        else:
            response = f"[Error] Type not available"
        reply = False
        return response, reply

    def get_response(self, prompt, type='chat'):
        """
        Get reponse from OpenAI GPT-3
        """
        default_prompt = f"\nHuman: {prompt}\nAI: "
        merged_prompt = default_prompt.format(prompt=prompt)
        self.current_prompt[self.type] += merged_prompt
        print(self.current_prompt)

        result = self.model.create(
            engine="davinci",
            prompt=self.current_prompt[type],
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["\n", " Human:", " AI:"]
        )

        response = result["choices"][0].text.replace(u'\xa0', u' ')

        self.current_prompt[self.type] = self.current_prompt[self.type] + response
        return response

    def do_command(self, command):
        """
        Execute command
        """
        response = None
        reply = True

        # command ex: $openai settype=chat
        if command.startswith("settype"):
            typed = command.split('=')[-1].lstrip().rstrip()
            response, reply = self.set_message_type(typed)
        else:
            # command ex: $openai "Hello"
            try:
                text = find_text(command) # find texts in double quotes

                lang = self.translator.detect_language(text)
                en_translated = self.translator.translate(text, src=lang, dest='en')

                en_response = self.get_response(en_translated, type=self.type)

                response = self.translator.translate(en_response, src='en', dest=lang)
                print(response)

            except Exception as e:
                response = "[Error] " + str(e)

        return response, reply