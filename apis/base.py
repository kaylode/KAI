import requests

class API:
    def __init__(self) -> None:
        self.triggers = ["$"]

    def do_command(self, command):
        pass

    def send_request(self, url, data, type, headers=None, **kwargs):
        if type == 'post':
            response = requests.post(url, data=data, headers=headers)
        elif type == 'get':
            response = requests.get(url, data=data, headers=headers)

        return self.process_response(response, **kwargs)

    def process_response(self, response, **kwargs):
        return response
