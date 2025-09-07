import discord
from discord.ext import commands
import json
import os
import asyncio
from bot.utils import load_config

# Get the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construct the absolute path to config.json
config_path = os.path.join(project_root, 'config.json')

config = load_config()
BOT_TOKEN = config.get("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.command()
async def ping(ctx):
    """Responds with 'Pong!'"""
    await ctx.send('Pong!')

async def load_cogs():
    """Loads all cogs from the cogs directory."""
    for filename in os.listdir(os.path.join(project_root, 'bot/cogs')):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'bot.cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load cog {filename[:-3]}: {e}')

def run_bot():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        print("Error: Bot token is not configured. Please add it to config.json.")
        return

    async def runner():
        async with bot:
            await load_cogs()
            await bot.start(BOT_TOKEN)

    asyncio.run(runner())


if __name__ == "__main__":
    run_bot()
