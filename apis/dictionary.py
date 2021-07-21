import random
from unidecode import unidecode
from replit import db

def clean_text(text):
    """
    Clean text:
        - Strip space at the beginning and ending
        - Remove Vietnamese accent
        - Lowercase
    """

    return unidecode(text.lstrip().rstrip().lower())


class Dictionary:
    """
    Dictionary for mapping special words in message
    """
    def __init__(self) -> None:
        self.trigger = ""
        self.db = None
        self.set_database(db)

    def set_database(self, database):
        """
        Use repl database for storing sentences
        """
        self.db = database
        if 'words' not in self.db.keys():
            self.db['words'] = {}

    def update_database(self, type, key, value):
        """
        Add more sentences to database
        """
        try:
            if key not in self.db[type].keys():
                self.db[type][key] = []
            self.db[type][key].append(value)
            response = "[Info] Updated database"
        except Exception as e:
            response = "[Error] " + str(e)
        return response, False

    def delete_database(self, type, key, index):
        """
        Delete sentences from database
        """
        try:
            self.db[type][key].pop(index)
        except Exception as e:
            response = "[Error] " + str(e)
        return response, False

    def random_response_from_list(self, responses):
        """
        Get random response from list of responses
        """
        return random.choice(responses)

    def format(self, string, dict):
        """
        Format a string
        """
        return string.format(**dict)
        
    def do_command(self, command, dict=None):
        """
        Execute command
        """
        response = None
        reply = False

        # If update command is used 
        if command.startswith("$updatew"):
            # Call example: $updatew hello KAI | hello there
            tokens = command.split('$updatew')
            key, value = tokens[-1].split('|')
            key =  clean_text(key)# No Vietnamese accent
            value = value.lstrip().rstrip()  
            response, reply = self.update_database('words',key,value)
        else:
            # Get list of responses based on keywords in database and user messages 
            responses_list = []
            for key, value in self.db['words'].items():
                command = clean_text(command)
                if key in command:
                    response = self.random_response_from_list(value)
                    responses_list.append(response)
            
            # One message can contain many keys in database, so choose randomly
            if len(responses_list) > 0:
                response = self.random_response_from_list(responses_list)
                response = self.format(response, dict)
            
        return response, reply
        
