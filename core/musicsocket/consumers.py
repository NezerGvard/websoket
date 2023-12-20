from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer

from core.settings import MEDIA_ROOT

import json
import os


class MusicConsumer(AsyncConsumer):

    channel_layer_alias = "echo_alias"

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        file_path = os.path.join(MEDIA_ROOT+'/sample-15s.wav')

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                audio_data = file.read()

                await self.send({
                    "type": "websocket.send",
                    "bytes": audio_data,
                })
        else:
            await self.send({
                "type": "websocket.send",
                "text": "File not found",
            })


    async def websocket_disconnect(self, event):
        pass


class UrlMusicConsumer(AsyncWebsocketConsumer):
    channel_layer_alias = "echo_alias"
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        file_url = os.path.join("http://212.22.85.36/media/sample-15s.wav")
        await self.send(text_data=file_url)