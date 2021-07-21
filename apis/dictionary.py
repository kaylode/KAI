import random
from replit import db

class Dictionary:
    def __init__(self) -> None:
        self.trigger = ""
        self.db = None
        self.set_database(db)

    def set_database(self, database):
        self.db = database
        if 'words' not in self.db.keys():
            self.db['words'] = {}

    def update_database(self, type, key, value):
        try:
            self.db[type][key] = value
            response = "[Info] Updated database"
        except Exception as e:
            response = "[Error] " + e

        return response, False

    def random_response_from_list(self, responses):
        return random.choice(responses)

    def do_command(self, command):
        
        if command.startswith("updatew"):
            tokens = command.split('updatew')
            key, value = tokens[-1].split('|')
            key = key.lstrip().rstrip()
            value = value.lstrip().rstrip()
            response, reply = self.update_database('words',key,value)
        else:
            responses_list = []
            for key, value in self.db['words'].items():
                if key in str.lower(command):
                    response = value
                    responses_list.append(response)
            
            response = self.random_response_from_list(responses_list)
            reply = False
        return response, reply
        
