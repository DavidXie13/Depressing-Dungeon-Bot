
import os
import sqlite3
import discord
import asyncio
import requests
import datetime
from bot_token import BOT_TOKEN
from bot_token import APPLICATION_ID
from discord.ext import tasks, commands
from functions import online_user_count
from functions import daily_fact
from database_functions import grant_exp
TOKEN = BOT_TOKEN

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = commands.Bot(command_prefix = '.', intents=intents, application_id = APPLICATION_ID)

@client.event
async def on_ready():
    print('{0.user} initiated'.format(client))
    db = sqlite3.connect('HiBot.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS main (user_id int, exp int, credits int, messages int, PRIMARY KEY (user_id))")

    online_user_count.start(client)
    daily_fact.start(client)

# Sync Slash Commands   
@client.command()
@commands.is_owner()
async def sync(ctx) -> None:
    synced = await ctx.bot.tree.sync()
    print(synced)
    await ctx.send(
        f"Synced **{len(synced)}** commands"
    )

# Remove Slash Commands   
@client.command()
@commands.is_owner()
async def remove(ctx):
    synced = await ctx.bot.tree.clear_commands()
    await ctx.send(
        f"Removed {len(synced)} commands"
    )

# Load Cog
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    print(f'{extension} has been loaded')

# Unload Cog
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    print(f'{extension} has been unloaded')

# Reload Cog
@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    print(f'{extension} has been reloaded')
    
# Load cogs on launch
async def load_extentions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == client.user and message.author.id != APPLICATION_ID:
        return
    else:
        print(f'({channel}) {username}: {user_message}')
        try:
            data = grant_exp(message.author.id, 1)
        except Exception as e:
            print(f"Error granting exp: {e}")

    await client.process_commands(message)


# New User
@client.event
async def on_member_join(member):
    if member.guild.id == 145502759997800449:
        try:
            role = discord.utils.get(member.guild.roles, name='Camel')
            await member.add_roles(role)
            print(f"{member} has joined the server")
        except Exception as e:
            print(f"Error: {member} joining server:\n{e}")
        await member.add_roles(role)
    
async def main():
    async with client:
        await load_extentions()
        await client.start(TOKEN)
asyncio.run(main())