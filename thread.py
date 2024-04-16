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
    forum_channel: discord.ForumChannel = bot.get_channel(1229627031323414546)  # Replace with your channel ID
    threads = await forum_channel.archived_threads().flatten()
    for thread in threads:
        await thread.delete()
    for root, dirs, files in os.walk('embeds'):
        # Sort the files numerically based on the prefix
        files.sort(key=lambda x: int(x.split('_')[0]), reverse=True)
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), encoding='utf-8') as f:
                    data = json.load(f)
                if 'thread_name' in data:
                    # Take the first field's name from the first embed
                    name = data['embeds'][0]['fields'][0]['name'] if 'name' in data['embeds'][0]['fields'][0] else "⠀"
                    thread = await forum_channel.create_thread(name=data['thread_name'], content=name)
                    logging.info(f'Created thread {data["thread_name"]}')
                    # Add a small delay to ensure the thread is ready to receive messages
                    await asyncio.sleep(1)
                    for embed_data in data['embeds']:
                        embed = discord.Embed.from_dict(embed_data)
                        await thread.send(embed=embed)
                        logging.info('Sent embed')

                # Move the file to the 'completed_embed' directory
                new_root = root.replace('embeds', 'completed_embeds')
                os.makedirs(new_root, exist_ok=True)
                shutil.move(os.path.join(root, filename), os.path.join(new_root, filename))
                logging.info(f'Moved {filename} to completed_embeds directory')

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
