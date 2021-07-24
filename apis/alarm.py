import pytz
import json
import random
from datetime import datetime

class Alarm:
    timezone = pytz.timezone('Asia/Saigon') # Set timezone to SG
    loop_second = 60              # Background task loop every x seconds
    def __init__(self) -> None:
      self.trigger = ""
      self.db = None
      db = self.load_database()
      self.set_database(db)

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
          if 'alarm' not in self.db.keys():
              self.db['alarm'] = {}

    def random_response_from_list(self, responses):
        """
        Get random response from list of responses
        """
        return random.choice(responses)

    def set_alarm(self, time, notification):
        """
        Set time alarm and save to database
        """
        if time not in self.db['alarm'].keys():
            self.db['alarm'][time] = []
        self.db['alarm'][time].append(notification)

    def check_alarm(self, time):
        """
        Check if time alarm, can be missed if loop_second is large, will look into it later
        """
        if time in self.db['alarm'].keys():
            responses = self.db['alarm'][time]
            response = self.random_response_from_list(responses)
        else:
            response = None
        return response

    def time_check(self): 
        """
        Reference: https://stackoverflow.com/questions/53755103/discord-py-time-schedule/53757482
        """

        now = datetime.strftime(datetime.now(Alarm.timezone), '%H:%M')
        response = self.check_alarm(now)
        return response