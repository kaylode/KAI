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
                    response, reply = api_object.do_command(command)
                else:
                    command = message.content
                    dict = {
                        'name': message.author.name
                    }
                    response, reply = api_object.do_command(command, dict)

                # Safe key for only one api is called at the time
                # If use more than one at the same time, consider removing this
                if response is not None:
                    break
                
        return response, reply

    def set_database(message, database):
        return super().set_database(database)



