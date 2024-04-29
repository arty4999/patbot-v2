import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

load_dotenv()

CHANNEL = os.getenv("CHANNEL")
TOKEN = os.getenv("TOKEN")
DISALLOWED_IDS = [int(id) for id in os.getenv("DISALLOWED_IDS").split(",")] if os.getenv("DISALLOWED_IDS") else []
REGEX = re.compile(r"(?i)((pls|plz|plis|please) )?pa+t me+( (pls|plz|plis|please))?")

intents = discord.Intents.default()
intents.messages = True  # This allows the bot to receive events about messages being sent and edited
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged on as', client.user)

@client.event
async def on_message(message):
        if not REGEX.match(message.content):
            if message.author.id in DISALLOWED_IDS:
                await message.delete()
        else:
            await message.channel.send(f"{message.author.mention} *pats*")
            print(f"Bot activated by {message.author} at {message.created_at}")

@client.event
async def on_message_edit(before, after):
    if after.channel.id == CHANNEL:
        if not REGEX.match(after.content):
            if after.author.id in DISALLOWED_IDS:
                await after.delete()
            else:
                print(f"Bot activated by {after.author} at {after.edited_at}")

client.run(TOKEN)