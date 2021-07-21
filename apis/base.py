import requests

class API:
    def __init__(self) -> None:
        self.trigger = "$"

    def do_command(self, command):
        pass

    def send_request(self, url, data, type, headers=None):
        if type == 'post':
            response = requests.post(url, data=data, headers=headers)
        elif type == 'get':
            pass

        return self.process_response(response)

    def process_response(self, response):
        return response
