import discord
import os
import requests
import base64
from io import BytesIO
import json 
from replit import db
from server import keep_alive

client = discord.Client()

url = "http://3a737b1df87f.ngrok.io/api"

def set_server_url(new_url):
    global url
    if new_url.endswith('api'):
        url = new_url
    else:
        url = new_url + 'api'

def get_prediction(image_url):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  
    data = {
      "url": image_url, 
      "model_types": 'yolov5m',
      'ensemble': False,
      'min_conf': 0.1,
      'min_iou': 0.5,
      'enhanced': False}

    payload = json.dumps(data)
    response = requests.post(url, data=payload, headers=headers)
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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$url'):
        global url
        new_url = message.content.split(' ')[-1]
        set_server_url(new_url)
        await message.channel.send(f'Server set at {url}')

    if message.content.startswith('$api'):
        image_url = message.content.split(' ')[-1]
        img_bytes, filename = get_prediction(image_url)
        if img_bytes:
            buffer = BytesIO(img_bytes)
            picture = discord.File(buffer, filename)
            await message.channel.send(file=picture)
        else:
            await message.channel.send('Fail to send image')



    if "responding" not in db.keys():
        db["responding"] = True

    

keep_alive()
TOKEN = os.getenv('TOKEN')
client.run(TOKEN)