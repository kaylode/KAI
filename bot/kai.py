from .base import Bot

class KAI(Bot):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.name = config.name

    def response(self, message):
        response = None
        reply = False
        
        for api_object in self.apis:
            if message.content.startswith(api_object.trigger):
                if api_object.trigger != '':
                    command = message.content.split(api_object.trigger)[-1].lstrip().rstrip()
                else:
                    command = message.content
                response, reply = api_object.do_command(command)
                break
        return response, reply

    def set_database(message, database):
        return super().set_database(database)



