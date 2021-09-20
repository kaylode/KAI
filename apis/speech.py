import speech_recognition as sr
# from googletrans import Translator

CACHE_DIR ='./.cache'

class SpeechToTextAPI:
    # translator = Translator()
    sr = sr.Recognizer()
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def speak(inpath=f'{CACHE_DIR}/recording.wav', lang="vi-VI"):
        
        # use the audio file as the audio source                                        
        with sr.AudioFile(inpath) as source:
            audio = SpeechToTextAPI.sr.record(source)               
            response = SpeechToTextAPI.sr.recognize_google(audio, language=lang)

        return response, True

