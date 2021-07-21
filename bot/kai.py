from .base import Bot

class KAI(Bot):
    """
    Source code of KAI 
    """
    def __init__(self, config) -> None:
        super().__init__(config)
        self.name = config.name

    def response(self, message):
        """
        How KAI response to message
        """
        response = None
        reply = False
        
        for api_object in self.apis:
            # If message contains trigger words
            if message.content.startswith(api_object.trigger):
                if api_object.trigger != '':
                    # Special calls
                    command = message.content.split(api_object.trigger)[-1].lstrip().rstrip() # Get and clean command
                    response, reply = api_object.do_command(command)    # Execute command
                else:
                    # Normal message, use dictionay to check
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



