import random

class Dictionary:
    def __init__(self) -> None:
        self.trigger = ""
        self.db = None

    def set_database(self, database):
        self.db = database

    def update_database(self, type, key, value):
        try:
            self.db[type][key] = value
            response = "Updated database"
        except Exception as e:
            response = e

        return response

    def random_response_from_list(self, responses):
        return random.choice(responses)

    def do_command(self, message):
        
        responses_list = []

        for key, value in self.db['words']:
            if key in str.lower(message.content):
                response = value
                responses_list.append(response)
        
        response = self.random_response_from_list(responses_list)

        return response
        
