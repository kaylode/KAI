import inspect
from .base import Bot

class KAI(Bot):
    """
    Source code of KAI 
    """
    def __init__(self, config, client) -> None:
        super().__init__(config, client)
        self.name = config.name

    async def response(self, message):
        """
        How KAI response to message
        """
        response = None
        reply = False
        
        for api_object in self.apis:
            for trigger in api_object.triggers:
                # If message contains trigger words
                tokens = message.content.split(' ')
                if tokens[0] == trigger:
                    if trigger != '':
                        # Special calls
                        command = message.content.split(trigger)[-1].lstrip().rstrip() # Get and clean command
                        
                        # Check if is async def function
                        if inspect.iscoroutinefunction(api_object.do_command):
                            response, reply = await api_object.do_command(command, trigger)
                        else:
                            response, reply = api_object.do_command(command, trigger)    # Execute command
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
            if response is not None:
                break
                
        return response, reply

    def set_database(message, database):
        return super().set_database(database)



