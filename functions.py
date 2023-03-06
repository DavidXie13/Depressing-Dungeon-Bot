import discord
import requests
import datetime
from random import randint
from discord.ext import tasks

# Check number of users online
@tasks.loop(minutes=5)
async def online_user_count(client):
    guild = client.get_guild(145502759997800449)
    now = datetime.datetime.now()
    online_user_count = 0
    for member in guild.members:
        if member.status != discord.Status.offline:
            online_user_count += 1
    print(f"{now.strftime('%Y-%m-%d %H:%M')} - Current number of online users: {online_user_count}")
    with open('log.txt', 'a') as file:
        file.write(f"{now.strftime('%Y-%m-%d %H:%M')} - Current number of online users: {online_user_count}\n")

@tasks.loop(minutes=1)
async def daily_minute_check(client):
    # Get current time:
    now = datetime.datetime.now()
    if int(now.hour) == 0 and int(now.minute) == 0:
        await daily_fact(client)
        await shiny_check(client)

async def daily_fact(client):
    # Get current time:
    channel = client.get_channel(145502759997800449)
    response = requests.get("https://uselessfacts.jsph.pl/random.json")

    if response.status_code == 200:
        data = response.json()
        fact = data["text"]
    else:
        print("Error: Request failed with status code", response.status_code)

    await channel.edit(topic=fact)
       
async def shiny_check(client):
    check = randint(1,4)
    print(f"Shiny Check: {check}")
    if check == 1:
        print("Shiny Found")
        with open("assets/shiny-psyduck.png", 'rb') as f:
            pic = f.read()
        nickname = 'Shiny Psyduck'
    else:
        with open("assets/psyduck.png", 'rb') as f:
            pic = f.read()
        nickname = 'Psyduck'

    try:
        guild = client.get_guild(145502759997800449)
        await guild.me.edit(nick = nickname)        
        await client.user.edit(avatar=pic)
    except Exception as e:
        print(f"Shiny Check Error: {e}")
        


