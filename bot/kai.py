from .base import Bot

class KAI(Bot):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.name = config.name

    def reponse(self, message):
        response = None
        for api_object in self.apis:
            if message.content.startswith(api_object.trigger):
                response = api_object.do_command(message)
                break
        return response

    def set_database(message, database):
        return super().set_database(database)



