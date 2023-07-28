# bot.py
import os
import discord
import requests
import time
import threading
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
STREAMER = os.getenv('STREAMER')

class TwitchBot(discord.Client):
    channel_to_send = None

    async def on_ready(self):
        print('Logged on as', self.user)
        for guild in client.guilds:
            for channel in guild.text_channels:
                member = guild.get_member(self.user.id)
                can_send_message = channel.permissions_for(member).send_messages
                if (can_send_message):
                    self.channel_to_send = channel
                    t = threading.Thread(target=loop, args=(asyncio.get_event_loop(),))
                    t.start()
    
    # Left this in for a little fun
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content == 'ping':
            await message.channel.send('pong')

def loop(event_loop):
    last = False
    while (True):
        status = checkStream()
        if (status == None):
            time.sleep(60)
        else:
            if (status == True and last == False):
                # Must be called this way in order to properly message
                asyncio.run_coroutine_threadsafe(client.channel_to_send.send("@everyone " + STREAMER + " IS LIVE!"), event_loop).result()
                print(STREAMER, "is live.")
            last = status
            time.sleep(60*10)

def checkStream():
    r = requests.get('https://www.twitch.tv/'+STREAMER)
    if (r.ok == False):
        print("Failed to GET request.")
        return None
    return "isLiveBroadcast" in r.content.decode('utf-8')

intents = discord.Intents.default()
intents.message_content = True
client = TwitchBot(intents=intents)
client.run(TOKEN)