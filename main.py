from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.errors import RPCError

from time import sleep

import wolframalpha
import configparser

app = Client("my_account")

@app.on_message(filters.command("type", prefixes='.') & filters.me)
def type(_, msg):
    msg_text = msg.text.split(".type ", maxsplit=1)[1]
    text = msg_text
    printed = ""

    while(printed != msg_text):
        try:
            printed = printed + text[0] 
            text = text[1:]
            
            try:
                msg.edit(printed)
            except Exception as e:
                pass
            else:
                sleep(0.05)
        except FloodWait as e:
            print(e)


client=None
@app.on_message(filters.command("Jarvis,", prefixes=""))
def alpha(_, msg):
    global client
    if client is None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        client = wolframalpha.Client(config['wolframalpha']['appId'])
        
    query = msg.text.split("Jarvis, ", maxsplit=1)[1] 
    res = client.query(query)
    msg.reply_text(next(res.results).text)


enableDarts=False
@app.on_message(filters.command("darts"))
def darts(_, msg):
    if not enableDarts:
        msg.reply_text("Darts disabled")
        return
    
    while True:
        try:
            sent = app.send_dice(chat_id=msg.chat.id, emoji="🎯")
        except RPCError as e:
            sleep(e.x)
            print(e)
        res = sent.dice.value

        if res == 6:
            break
        else:
            try:
                sent.delete()
                sleep(1)
            except RPCError as e:
                sleep(e.x)
                print(e)


@app.on_message(filters.command("disableDarts"))
def disable_darts(_, msg):
    global enableDarts
    enableDarts=False


@app.on_message(filters.command("enableDarts"))
def enable_darts(_, msg):
    global enableDarts
    enableDarts=True


@app.on_message(filters.command("clearDarts"))
def clear_darts(_, msg):
    found = app.search_messages(msg.chat.id, from_user=msg.from_user.username, limit=100)
    for message in found:
        if not message.dice is None and message.dice.emoji=="🎯":
            try:
                message.delete()
                sleep(1)
            except RPCError as e:
                sleep(e.x)
                print(e)
app.run()
