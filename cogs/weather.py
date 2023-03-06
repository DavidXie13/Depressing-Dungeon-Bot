import discord
import requests
from discord import app_commands
from discord.ext import commands
from bot_token import WEATHER_API_KEY

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="weather", 
                          description="Get the current weather in Melbourne, Australia")
    async def weather(self, interaction: discord.Interaction):
        #channel_id = interaction.channel
        try:
            country = 'AU'
            city = 'Melbourne'

            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={WEATHER_API_KEY}"

            response = requests.get(url)
            data = response.json()

            temperature = data['main']['feels_like']
        except Exception as e:
            await interaction.response.send_message("An error has occured whilst retrieving the weather")
            print(f"Weather API Error: {e}")
        await interaction.response.send_message(f"It is currently **{temperature}** degrees in **Melbourne, Australia**")

async def setup(client):
    await client.add_cog(Weather(client))