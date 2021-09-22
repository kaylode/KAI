import random
from unidecode import unidecode
import json
import datetime
import pytz

# set timezone asia/saigon
tz = pytz.timezone("Asia/Saigon")


def clean_text(text):
    """
    Clean text:
        - Strip space at the beginning and ending
        - Remove Vietnamese accent
        - Lowercase
    """
    return text
    # return unidecode(text.lstrip().rstrip().lower())


class Dictionary:
    """
    Dictionary for mapping special words in message
    """
    def __init__(self) -> None:
        self.trigger = ""
        self.db = None
        db = self.load_database()
        self.set_database(db)

    def save_database(self, path='./database/db.json'):
        """
        Save database to json file
        """
        with open(path, 'w') as f:
            json.dump(self.db, f)
        
        response = "[Info] Saved database"
        return response, False

    def load_database(self, path='./database/db.json'):
        """
        Load database from json
        """
        with open(path, 'r') as f:
            data = json.load(f)
        return data
        
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
            if type not in self.db.keys():
                self.db[type] = {}
            if key not in self.db[type].keys():
                self.db[type][key] = []
            self.db[type][key].append(value)
            response = "[Info] Updated database"
        except Exception as e:
            response = "[Error] " + str(e)
        return response, False

    def list_db(self, type):
        """
        List data from database
        """
        if type == '':
            response_dict = self.db
        else:
            response_dict = self.db[type]
        response = str(response_dict)
        return response, False

    def delete_database(self, type, key, index):
        """
        Delete sentences from database
        """
        try:
            if index is None:
                del self.db[type][key]
            else:
                index = int(index)
                self.db[type][key].pop(index)
            response = "[Info] Deleted from database"
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

        try:
            # If update command is used 
            if command.startswith("$updatedb"):
                # Call example: $updatedb words | hello KAI | hello there
                tokens = command.split('$updatedb')
                k_type, key, value = tokens[-1].split('|')
                key =  clean_text(key)# No Vietnamese accent
                value = value.lstrip().rstrip()
                k_type = k_type.lstrip().rstrip()  
                response, reply = self.update_database(k_type,key,value)
            elif command.startswith("$deletedb"):
                # Call example: $deletedb words | hello KAI | 1
                tokens = command.split('$deletedb')
                tokens = tokens[-1].split('|')
                if len(tokens) == 2:
                    k_type, key = tokens
                    index = None
                if len(tokens) == 3:
                    k_type, key, index = tokens
                key =  key.lstrip().rstrip()
                if index is not None:
                    index = index.lstrip().rstrip() 
                k_type = k_type.lstrip().rstrip()  
                response, reply = self.delete_database(k_type,key,index)
            elif command.startswith("$savedb"):
                response, reply = self.save_database()
            elif command.startswith("$gettime"):
                #Get current time
                response = datetime.datetime.now(tz)
                reply = False
            elif command.startswith("$listdb"):
                # Call example: $listdb words
                tokens = command.split('$listdb')
                type = tokens[-1].lstrip().rstrip()
                response, reply = self.list_db(type)
            elif not command.startswith("$"):
                # Get list of responses based on keywords in database and user messages 
                responses_list = []
                for key, value in self.db['words'].items():
                    command = clean_text(command)
                    if key in command:
                        reply = True
                        response = self.random_response_from_list(value)
                        responses_list.append(response)
                
                # One message can contain many keys in database, so choose randomly
                if len(responses_list) > 0:
                    response = self.random_response_from_list(responses_list)
                    response = self.format(response, dict)
                    reply = True
        
        except Exception as e:
            response = "[Error] " + str(e)
            reply = False
            
        return response, reply
        
