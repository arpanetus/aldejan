import asyncio
from typing import Any, Callable
from pyrogram import Client, filters
from pyrogram.methods.chats import Chats
from pyrogram.types import Message
from selector import Selector, MsgDecs
import os


BOT_TOKEN = os.environ.get("BOT_TOKEN", "nonetoken")
API_ID = os.environ.get("API_ID", "noneapiid")
API_HASH = os.environ.get("API_HASH", "noneapihash")
CHAT_ID = int(os.environ.get("CHAT_ID", "-1"))

app = Client(
    "bot-client",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

import hashlib

m = hashlib.sha256()
m.update(str(API_ID + API_HASH + BOT_TOKEN + str(CHAT_ID)).encode())

print(str(m.hexdigest()))

guidelines = """Hello, {user}!
Your channel was already assigned to this bot. 
Now it's a time to do some lottery!.

Only admins can run the commands below:
/start - shows this message
/list - allows admins to see members of his channel in a listed manner (note that there might be several messages).
/winner - chooses the winner among the members which are neither admins nor banned,restricted,etc..
"""

s = Selector(app, CHAT_ID)
d = MsgDecs()


async def wrap_access_or_anything(f, msg: Message) -> None:
    try:
        await f()
    except Exception as e:
        print(e.with_traceback())
        await msg.reply_text("i can't connect to the channel, ask my creator fix me, sempai 🥺")
    


@app.on_message(filters.text & filters.private)
async def handler(client: Client, message: Message):
    if message.text == "/debug":
        await message.reply_text("i kinda work tho 🤔")

    async def do():
        if message.from_user.id not in [
            mem.user.id for mem in (await s.get_admin_members())
        ]:
            await message.reply_text(
                "[fug off:D](https://i.kym-cdn.com/photos/images/newsfeed/001/175/637/16d.jpg)"
            )

            return
        if message.text == "/start":
            await message.reply_text(guidelines.format(user=message.from_user.mention))
        if message.text == "/list":
            for chunk in d.list_view_as_md(d.filter_members(await s.get_members())):
                await message.reply_text(chunk)
        if message.text == "/winner":
            winner = d.choose_one_from(d.filter_members(await s.get_members()))
            await message.reply_text(d.aqalay_maqalay())
            for i in d.down_counter(3):
                await message.reply_text(f"{i}...")
                await asyncio.sleep(i)
            await client.send_message(CHAT_ID, d.decorate_winner(winner))

    await wrap_access_or_anything(do, message)


app.run()
