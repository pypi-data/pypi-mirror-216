import json
import time
import random
import base64
import requests
import websocket
from requests.structures import CaseInsensitiveDict
from threading import Thread
from .utils.payloads import StartSocket
from .utils.objects import MessageContent


class SocketDiscord:
    def __init__(self, client):
        self.events = {}
        self.ws = None
        self.token = client.token

    def on(self, event):
        def event_ready(handler):
            if event not in self.events:
                self.events[event] = []
            self.events[event].append(handler)
            return handler
        return event_ready

    def trig(self, event, *args, **kwargs):
        if event in self.events:
            for handler in self.events[event]:
                handler(*args, **kwargs)

    def send_json(self, payload):
      self.ws.send(json.dumps(payload))

    def receive_json(self):
      response = self.ws.recv()
      if response:
        return json.loads(response)

    def heartbeat(self):
      timer = 40
      payload = {
      "op": 1,
      "d": None
    }
      while True:
        time.sleep(timer)
        self.send_json(payload)

    def start_ws(self):
      self.ws = websocket.WebSocket()
      self.ws.connect('wss://gateway.discord.gg/?encoding=json')
      self.send_json(StartSocket(self.token))
      Thread(target=self.event_manager).start()
      self.session_id = self.receive_json()
      self.session_id = self.session_id.get('d').get('session_id')

    def get_object(self, data):
      if data['t'] == 'MESSAGE_CREATE':
        return MessageContent(data).MessageContent
      
      return data
      
    def event_manager(self):
      while True:
        event = self.receive_json()
        try:
            self.trig('all', event)
            self.trig(event['t'], self.get_object(event))
        except:
            self.trig('others', event)