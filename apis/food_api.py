import json
import requests
import base64
from io import BytesIO

from .base import API
import discord

class FoodAPI(API):
    """
    Food detection API 
    https://github.com/kaylode/yolov5-meal-analysis
    """
    def __init__(self) -> None:
        super().__init__()
        self.triggers = ["$food"]
        self.url = ""

    def do_command(self, command):
        """
        Execute command
        """
        response = None
        reply = False

        # Set API url (because this API url not stable)
        # Example call: $food url google.com
        if command.startswith("url"):
            new_url = command.split('url')[-1].lstrip().rstrip()
            response = f'[Info] Server set at {new_url}'
            reply = False
            self.set_server_url(new_url)

        # After set url, start predicting on image url
        # Example call: $food predict https://xxxx/food.png
        if command.startswith('predict'):
            image_url = command.split('predict')[-1]

            # Construct discord File from buffer and filename
            response = self.get_prediction(image_url)

            if response is not None:
                buffer, filename = response
                response = discord.File(buffer, filename)
            else:
                response = "[Error] Wrong server url or server is inaccessible right now" 
            reply = False

        return response, reply

    def set_server_url(self, new_url):
        """
        Set API server url
        """
        self.url = new_url

    def send_request(self, url, data, type, headers):
        """
        Send request API call
        """
        return super().send_request(url, data, type, headers=headers)
    
    def process_response(self, response):
        """
        Process response from server
        """
        try:
            data = response.json()  
            # Code: 200 means success
            if data['code'] == 200:
                # convert it into bytes  
                im_b64 = data['res_image']
                filename = data['filename']
                # Decode image from base64 string
                img_bytes = base64.b64decode(im_b64.encode('utf-8'))
                return img_bytes, filename
            else:
                return None              
        except requests.exceptions.RequestException:
            return None

    def get_prediction(self, image_url):
        """
        Main method to send request and return buffer of result image
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # To change detection model hyperparams, change these number
        data = {
            "url": image_url, 
            "model_types": 'yolov5m',
            'ensemble': True,
            'min_conf': 0.15,
            'min_iou': 0.5,
            'enhanced': False}

        payload = json.dumps(data)

        # Send request
        response = self.send_request(self.url, payload, type='post', headers=headers)
        if response is not None:
            # Bytes received, store to buffer
            img_bytes, filename = response
            if img_bytes:
                buffer = BytesIO(img_bytes)
                return buffer, filename
            else:
                return None
        else:
            return None
            