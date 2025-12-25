import discord
from discord.ext import commands
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DATA_FILE = "bot_config.json"

# --- Data Persistence ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"disallowed_ids": [], "guarded_channels": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_data()

# --- Bot Setup ---
REGEX = re.compile(
    r"(?i)\b((pls|plz|plis|ple+ase|pwease|plez|ple+ez) )?(pa+t|pwat) (me|mwe)+( (pls|plz|plis|ple+ase|plez|ple+ez))?\b"
)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Headpatting the world"))

async def check_and_pat(message):
    if message.author.bot:
        return

    is_pat_request = REGEX.search(message.content)

    if is_pat_request:
        await message.channel.send(f"{message.author.mention} *pats*")
    else:
        # LOGIC: If no channels are guarded, check everywhere. 
        # If channels ARE guarded, only check if we are in one of them.
        is_guarded_zone = len(config["guarded_channels"]) == 0 or message.channel.id in config["guarded_channels"]
        
        if is_guarded_zone and message.author.id in config["disallowed_ids"]:
            try:
                await message.delete()
            except discord.Forbidden:
                pass

# --- Events ---
@bot.event
async def on_message(message):
    await check_and_pat(message)
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await check_and_pat(after)

# --- Commands for Users ---
@bot.command()
@commands.has_permissions(manage_messages=True)
async def disallow(ctx, user: discord.Member):
    if user.id not in config["disallowed_ids"]:
        config["disallowed_ids"].append(user.id)
        save_data(config)
        await ctx.send(f"✅ {user.display_name} is now restricted.")
    else:
        await ctx.send("ℹ️ User is already restricted.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def allow(ctx, user: discord.Member):
    if user.id in config["disallowed_ids"]:
        config["disallowed_ids"].remove(user.id)
        save_data(config)
        await ctx.send(f"✅ {user.display_name} is no longer restricted.")
    else:
        await ctx.send("ℹ️ User was not restricted.")

# --- Commands for Channels ---
@bot.command()
@commands.has_permissions(manage_guild=True)
async def guard(ctx):
    """Sets the current channel as a guarded zone."""
    if ctx.channel.id not in config["guarded_channels"]:
        config["guarded_channels"].append(ctx.channel.id)
        save_data(config)
        await ctx.send(f"🛡️ This channel is now guarded. Restricted users must ask for pats or their messages will be deleted.")
    else:
        await ctx.send("ℹ️ This channel is already being guarded.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def unguard(ctx):
    """Removes the guard from the current channel."""
    if ctx.channel.id in config["guarded_channels"]:
        config["guarded_channels"].remove(ctx.channel.id)
        save_data(config)
        await ctx.send("🔓 This channel is no longer guarded.")
    else:
        await ctx.send("ℹ️ This channel wasn't being guarded.")

bot.run(TOKEN)
