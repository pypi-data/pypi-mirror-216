import json
import time
import random
import base64
import requests
import websocket
from requests.structures import CaseInsensitiveDict
from threading import Thread
from user_discord.utils.payloads import StartSocket
from user_discord.utils.objects import MessageContent


class ClientDiscord:

  def __init__(self):
    
    self.token = None

    self.username = None
    self.email = None
    self.id = None
    self.telephone = None

    self.headers = CaseInsensitiveDict()


  def generate_nonce(self):
    return str(random.randint(1121966494243094528, 2121966494243094528))

  def login_token(self, token):
    # "Login" in account with token
    global requests
    api = "https://discord.com/api/users/@me"
    temp_headers = CaseInsensitiveDict()
    temp_headers['Authorization'] = token
    res = requests.get(api, headers=temp_headers)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      data = res.json()
      self.headers['Authorization'] = token
      self.web = requests.Session()
      self.web.headers = self.headers
      self.username = data['username']
      self.id = data['id']
      self.email = data['email']
      self.telephone = data['phone']
      self.token = token
      return data

  def send_message(self, channelId, message):
    #Send message in channel
    api = f"https://discord.com/api/v9/channels/{channelId}/messages"
    payload = {
      "content": message,
      "flags": 0,
      "nonce": self.generate_nonce(),
      "tts": False
    }
    res = self.web.post(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()
      
  def delete_message(self,channelId, messageId):
    #Delete a message by channel and message id
    api = f"https://discord.com/api/v9/channels/{channelId}/messages/{messageId}"
    res = self.web.delete(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.status_code

  def get_dms(self):
    #Get a list of users in DM
    api = "https://discordapp.com/api/users/@me/channels"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def get_servers(self):
    # Get a list of your servers
    api = "https://discord.com/api/users/@me/guilds"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def get_friends(self):
    # Get a list of your friends
    api = "https://discord.com/api/users/@me/relationships"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def get_channel_messages(self, channelId, limit: int = 50):
    #Get a list of messages in channel
    api = f"https://discord.com/api/v9/channels/{channelId}/messages?limit={limit}"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def set_status(self, status, content: str = None, emoji: str = None):
    #Set user status
    api = "https://discord.com/api/v9/users/@me/settings"
    payload = {"status": status, "custom_status":{"text":content,"emoji_name":emoji}}
    res = self.web.patch(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def set_bio(self, content):
    #Set user bio
    api = "https://discord.com/api/v9/users/@me/profile"
    payload = {"bio": content}
    res = self.web.patch(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def set_avatar(self, url):
    #Change user avatar by url
    image_data = requests.get(url).content
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    data = f"data:image/png;base64,{image_b64}"

    api = "https://discord.com/api/v9/users/@me"
    payload = {"avatar": data}
    res = self.web.patch(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()