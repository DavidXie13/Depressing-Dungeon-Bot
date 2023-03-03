import discord
import requests
import datetime
from discord.ext import tasks

# Check number of users online
@tasks.loop(minutes=5)
async def online_user_count(client):
    guild = client.get_guild(145502759997800449)
    online_user_count = 0
    for member in guild.members:
        if member.status != discord.Status.offline:
            online_user_count += 1
    print(f"Current number of online users: {online_user_count}")

@tasks.loop(minutes=1)
async def daily_fact(client):
    # Get current time:
    now = datetime.datetime.now()
    channel = client.get_channel(145502759997800449)
    if int(now.hour) == 0 and int(now.minute) == 0:
        response = requests.get("https://uselessfacts.jsph.pl/random.json")

        if response.status_code == 200:
            data = response.json()
            fact = data["text"]
        else:
            print("Error: Request failed with status code", response.status_code)

        await channel.edit(topic=fact)


