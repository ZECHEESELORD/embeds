import discord
import os
import json
import logging
from dotenv import load_dotenv
import shutil
import asyncio

load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.reactions = True

bot = discord.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    
    # Prompt for a JSON file
    json_file = input("Please enter the path to the JSON file (relative to the /embeds/ directory): ")
    json_file = os.path.join('embeds', json_file)
    
    # Prompt for a channel ID
    channel_id = input("Please enter the channel ID: ")
    channel: discord.TextChannel = bot.get_channel(int(channel_id))
    
    # Load the JSON data
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    
    # Send the embeds
    for embed_data in data['embeds']:
        embed = discord.Embed.from_dict(embed_data)
        await channel.send(embed=embed)
        logging.info('Sent embed')


bot.run(os.getenv('DISCORD_BOT_TOKEN'))
