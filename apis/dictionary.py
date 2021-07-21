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
            if key not in self.db[type].keys():
                self.db[type][key] = []
            self.db[type][key].append(value)
            response = "[Info] Updated database"
        except Exception as e:
            response = "[Error] " + str(e)
        return response, False

    def delete_database(self, type, key, index):
        try:
            self.db[type][key].pop(index)
        except Exception as e:
            response = "[Error] " + str(e)
        return response, False

    def random_response_from_list(self, responses):
        return random.choice(responses)

    def format(self, string, dict):
        return string.format(**dict)
        
    def do_command(self, command, dict=None):
        
        response = None
        reply = False
        if command.startswith("$updatew"):
            tokens = command.split('$updatew')
            key, value = tokens[-1].split('|')
            key = key.lstrip().rstrip().lower()
            value = value.lstrip().rstrip()
            response, reply = self.update_database('words',key,value)
        else:
            responses_list = []
            for key, value in self.db['words'].items():
                if key in str.lower(command):
                    response = self.random_response_from_list(value)
                    responses_list.append(response)
            
            if len(responses_list) > 0:
                response = self.random_response_from_list(responses_list)
                response = self.format(response, dict)
            
        return response, reply
        
