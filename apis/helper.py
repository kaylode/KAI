

help_dict = {
    'food': {
        'url': "Set ngrok server API",
        'predict': "Detect food from image"
    },
    'translate': 'Translate a text in double quotes. Example: $translate "hello"',
}

class Helper:
    """
    Helper class for printing BOT information
    """
    def __init__(self) -> None:
        self.trigger = "$help"

    def do_command(self, command):
        """
        Execute command
        """
        response = None
        reply = False
    
        for key in help_dict.keys():
            command = command.rstrip().lstrip()
            if command == key or command == "":
                response = f"{key}: "
                details = help_dict[key] # Dict or string
                if isinstance(details, dict):
                    response += "\n"
                    for key2, value in details.items():
                        response += f"\t{key2}: {value}\n"
                else:
                    response += f"{details}\n"

        return response, reply