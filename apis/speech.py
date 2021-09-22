import speech_recognition as sr
# from googletrans import Translator

CACHE_DIR ='./.cache'

def process_response(text):
    text = text.lower()
    tokens = text.split()
    if tokens[0] == 'play':
        return '$play ' + ' '.join(tokens[1:])
    else:
        return None


class SpeechToTextAPI:
    """
    Speech to text, load from wav file
    https://github.com/Uberi/speech_recognition
    """
    # translator = Translator()
    sr = sr.Recognizer()
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def speak(inpath=f'{CACHE_DIR}/recording.wav', lang="vi-VI"):
        
        # use the audio file as the audio source     
        try:              
            with sr.AudioFile(inpath) as source:
                audio = SpeechToTextAPI.sr.record(source) 
                response = SpeechToTextAPI.sr.recognize_google(audio, language=lang)
        except:
            response = None

        if response is not None:
            response = process_response(response)
        return response

