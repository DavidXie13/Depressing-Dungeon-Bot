import os
import time
import random
import discord
from discord import app_commands
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Queue to add songs to:
        self.queue = []
        self.voice_channel = None
        self.channel_id = None

    @app_commands.command(name="play", 
                          description="Play music")
    async def play(self, interaction : discord.Interaction):
        self.channel_id = interaction.channel
        
        # Check if already playing music:
        if self.queue and self.voice_channel is not None:
            await interaction.response.send_message("The bot is already playing music")
            return

        # Get voice channel of user:
        try:
            voice_channel = interaction.user.voice.channel
            print(f"Channel detected:: {voice_channel}")
        except Exception as e:
            print(f"Channel detected error:: {e}")
            await interaction.response.send_message("You are not in a voice channel")
            return

        # Connect to voice channel
        if self.voice_channel is None:
            try:
                self.voice_channel = await voice_channel.connect()
            except Exception as e:
                print(f"Connection Error: {e}")
        else:
            await self.voice_channel.move_to(voice_channel)

        songs = os.listdir("Music")
        random.shuffle(songs)
        await interaction.response.send_message("Bot will begin playing music")
        
        # Queue songs
        for song in songs:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('Music/' + song), volume = 0.5)
            title = song.split(".")
            title = ".".join(title[:-1])

            self.queue.append((source, title))

        try:
            vc = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
            await self.play_next_song(vc)
        except Exception as e:
            print(f"Play Error: {e}")

    @app_commands.command(name="stop", description="Stop playing music and clear queue")
    async def stop(self, interaction: discord.Interaction):
        try:
            if self.voice_channel is not None:
                await self.voice_channel.disconnect()
                self.voice_channel = None
                self.queue.clear()
                await interaction.response.send_message("Bot will now stop playing music")
        except Exception as e:
            print(f"Stop Error: {e}")

    # Command to skip the current song and go to the next song
    @app_commands.command(name="skip", description="Skip to the next song")
    async def skip(self, interaction: discord.Interaction):
        if self.voice_channel is None:
            print("Skip Failed: No Channel")
            return
        if not self.queue:
            await interaction.response.send_message("Already at end of queue")
            print("Skip Failed: No Queue")
            return
        try:
            self.voice_channel.stop()
            await interaction.response.send_message("Skipping to next song")
        except Exception as e:
            print(f"Skip Error: {e}")

    # Check if the bot has been disconnected from the voice channel
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.client.user.id and before.channel is not None and after.channel is None:
            self.queue.clear()
            self.voice_channel = None
            self.channel_id = None
            print(f"Bot Disconnected from {before.channel}")

    # Function to loop through the queue
    async def play_next_song(self, vc):
        if len(self.queue) > 0:
            try:
                source, title = self.queue.pop(0)
                vc.play(source, after=lambda e: self.client.loop.create_task(self.play_next_song(vc)))
                await self.channel_id.send(f"Now Playing: **{title}**")
            except Exception as e:
                print(f"Play_next_song Function Error: {e}")
        else:
            
            if self.voice_channel is not None:            
                await self.channel_id.send("Bot will now stop playing music")
                await self.voice_channel.disconnect()
            self.voice_channel = None
            self.queue.clear()
        time.sleep(2)

    # debug command
    @commands.command()
    async def debug(self, ctx):
        print("===== Debug =====")
        print(f"Voice Channel: {self.voice_channel}\nQueue: {self.queue}\nChannel_id: {self.channel_id}")
        print("=================")

async def setup(client):
    await client.add_cog(Music(client))
