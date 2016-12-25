from bot.utils import process
import sys
import time
import telepot
import json

TOKEN = '308125138:AAFltHYK_wgKgSmxMzgCC60UL7Er1D14jlE'

def handle(message):
    message_id = message['message_id']
    chat = message['chat']
    chat_id = chat['id']
    if 'text' in message:
        process(chat_id, message=message['text'])
    if 'location' in message:
        process(chat_id, location=message['location'])
    if 'contact' in message:
        process(chat_id, contact=message['contact'])
    return "OK"


bot = telepot.Bot(TOKEN)
bot.message_loop(handle)


# Keep the program running.
while 1:
    time.sleep(10)