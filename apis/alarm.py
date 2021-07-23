import pytz
import json
from datetime import datetime
from discord.ext import tasks, commands

class Alarm:
    timezone = pytz.timezone('Asia/Saigon') # Set timezone to SG
    loop_second = 10              # Loop every x seconds
    def __init__(self) -> None:
      self.trigger = ""
      self.db = None
      db = self.load_database()
      self.set_database(db)
      self.morning = self.db['alarm']['morning']
      self.noon = self.db['alarm']['noon']
      self.afternoon = self.db['alarm']['afternoon']
      self.evening = self.db['alarm']['evening']

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

    @staticmethod
    def time_check(): 
        """
        Reference: https://stackoverflow.com/questions/53755103/discord-py-time-schedule/53757482
        """

        now = datetime.strftime(datetime.now(Alarm.timezone), '%H:%M')
        messages = ('thang @Scuola Pera nhu cac')
        messages = str(now)

        return messages