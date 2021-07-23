

help_dict = {
    '$help': "\t\t\t\t Print usage guide of commands",
    '$translate': '\t\t\tTranslate text in double quotes. Ex: $translate "hello"',
    '$speak': '\t\t\t\tSpeak a message. Ex: $speak "hello"',
    '$voice': '\t\t\t\tWhether to reply using voice. Ex: $voice on',
    '$ai': {
        'url': "\t\t\t\tSet ngrok server API",
        'detect': "\t\t\tDetect objects from image"
    },
    '$food': {
        'url': "\t\t\t\tSet ngrok server API",
        'predict': "\t\t\tDetect food from image"
    },
    '$gettime': '\t\t\tGet system time'
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
        reply = False

        response = ""
        for key in help_dict.keys():
            command = command.rstrip().lstrip()
            if command == key or command == "":
                response += f"{key}: "
                details = help_dict[key] # Dict or string
                if isinstance(details, dict):
                    response += "\n"
                    for key2, value in details.items():
                        response += f"\t{key2}: {value}\n"
                else:
                    response += f"{details}\n"

        return response, reply