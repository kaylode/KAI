import discord
import os
import requests
import json
from replit import db
from server import keep_alive

client = discord.Client()

def get_prediction(image_path):
    data = {"image": image_path}
    url = "http://3a737b1df87f.ngrok.io/api"
    response = requests.post(url, data)
    if response.ok:
        print(response.json())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$api'):
        get_prediction("test.png")


    if "responding" not in db.keys():
        db["responding"] = True

    # with open('my_image.png', 'rb') as f:
    #     picture = discord.File(f)
    #     await channel.send(file=picture)

keep_alive()
TOKEN = os.getenv('TOKEN')
client.run(TOKEN)