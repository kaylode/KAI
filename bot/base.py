from apis import get_api

class Bot:
    """
    Abstract class for Discord bot
    """
    def __init__(self, config, client) -> None:
        self.config = config
        self.apis = []
        self.client = client

        # Init all apis instances
        self.init_features()

    def init_features(self):
        for api_name in self.config.apis:
            api_instance = get_api(api_name, self.client)
            self.apis.append(api_instance)

    def reponse(self, message):
        reply = False
        response = message

        return response, reply

    def set_database(message, database):
        pass

    


