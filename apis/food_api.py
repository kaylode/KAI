import json
import requests
import base64
from io import BytesIO

from .base import API
import discord

class FoodAPI(API):
    def __init__(self) -> None:
        super().__init__()
        self.trigger = "$food"
        self.url = "http://3a737b1df87f.ngrok.io/api"

    def do_command(self, command):
        if command.startswith("url"):
            new_url = command.split('url')[-1]
            response = f'Server set at {new_url}'
            reply = False
            self.set_server_url(new_url)

        if command.startswith('predict'):
            image_url = command.split('predict')[-1]
            buffer, filename = self.get_prediction(image_url)
            response = discord.File(buffer, filename)
            reply = False

        return response, reply

    def set_server_url(self, new_url):
        self.url = new_url

    def send_request(self, url, data, type, headers):
        return super().send_request(url, data, type, headers=headers)
    
    def process_response(self, response):
        try:
            data = response.json()  
            print(data['code'])   
            if data['code'] == 200:
                # convert it into bytes  
                im_b64 = data['res_image']
                filename = data['filename']
                img_bytes = base64.b64decode(im_b64.encode('utf-8'))
                return img_bytes, filename
            else:
                return None              
        except requests.exceptions.RequestException:
            return None

    def get_prediction(self, image_url):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
        data = {
            "url": image_url, 
            "model_types": 'yolov5m',
            'ensemble': False,
            'min_conf': 0.1,
            'min_iou': 0.5,
            'enhanced': False}

        payload = json.dumps(data)
        
        img_bytes, filename = self.send_request(self, self.url, payload, type='post', headers=headers)
        if img_bytes:
            buffer = BytesIO(img_bytes)

        return buffer, filename
            