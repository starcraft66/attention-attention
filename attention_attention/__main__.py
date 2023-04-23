# Copyright (C) Tristan Gosselin-Hane
# This file is part of attention-attention <https://github.com/starcraft66/attention-attention>.
#
# attention-attention is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# attention-attention is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with attention-attention.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import os
import importlib.resources

import attention_attention
import discord
from discord import app_commands
from discord.ext import commands
import aiocron
import datetime

def get_media_path(path):
    return importlib.resources.files(__package__ + ".media") / path


class Announcement():
    def __init__(self, hour, minute, audio_file):
        self.hour = hour
        self.minute = minute
        self.audio_file = audio_file


class AttentionAttention(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self._announcements = [
            Announcement(1, 45, get_media_path("attention-attention.mp3")),
            Announcement(2, 0, get_media_path("attention-attention-2.mp3")),
        ]
        for anc in self._announcements:
            aiocron.crontab(f"{anc.minute} {anc.hour} * * *", func=self.attention, args=[anc.audio_file], start=True)

    async def owner_only(interaction: discord.Interaction):
        return await interaction.client.is_owner(interaction.user)

    @app_commands.command(name="attention")
    async def attention_cmd(self, interaction: discord.Interaction) -> None:
        """ /attention """
        await interaction.response.send_message("Attention! Attention!")

    @app_commands.command(name="about")
    async def about_cmd(self, interaction: discord.Interaction) -> None:
        """ /about """
        await interaction.response.send_message(f"Attention! Attention! {attention_attention.__version__}\nInvite link: {discord.utils.oauth_url(client_id=self.bot.user.id)}", ephemeral=True)

    @app_commands.command(name="sync")
    @app_commands.guilds(discord.Object(id=499989296451944489)) # Hera Ca$h Money CorPoration
    @app_commands.check(owner_only)
    async def sync_cmd(self, interaction: discord.Interaction) -> None:
        """ /sync """
        await interaction.response.send_message("Syncing the command tree now...")
        print("Performing command tree sync")
        await self.bot.tree.sync()
        await self.bot.tree.sync(guild=discord.Object(id=499989296451944489))
        print("Completed command tree sync")

    async def attention(self, audio_file):
        vcs_to_play = []
        for guild in self.bot.guilds:
            most_populated_vc = max(guild.voice_channels, key=lambda x: len(x.members))
            if len(most_populated_vc.members) == 0:
                continue
            vcs_to_play.append(most_populated_vc)

        await asyncio.gather(*[self.play_attention_attention(audio_file, vc) for vc in vcs_to_play])

    async def play_attention_attention(self, audio_file, voice_channel):
        if voice_channel is not None:
            voice_client: discord.VoiceClient = await voice_channel.connect()
            audio_source = discord.FFmpegPCMAudio(audio_file)
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()

async def main():
    print(f"libopus loaded status: {discord.opus.is_loaded()}")
    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(command_prefix=commands.when_mentioned_or("!attention"),
                    description="ATTENTION! ATTENTION!",
                    intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} ({bot.user.id})")
        print(f"Discord bot invite link: {discord.utils.oauth_url(client_id=bot.user.id)}")
        print(f"The bot is in {len(bot.guilds)} guilds: {', '.join([guild.name for guild in bot.guilds])}")
        if (os.getenv("DISCORD_COMMAND_SYNC")):
            print("Performing initial command tree sync")
            await bot.tree.sync()
            await bot.tree.sync(guild=discord.Object(id=499989296451944489))
            print("Completed initial command tree sync")

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("DISCORD_TOKEN environment variable is missing!")
        exit()

    await bot.add_cog(AttentionAttention(bot))
    await bot.start(token)

if __name__ == "__main__":
    print("Attention! Attention! " + attention_attention.__version__ + " starting!")
    print(f"Current time zone: {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}")

    if not discord.opus._load_default():
        discord.opus.load_opus(os.getenv("LIBOPUS_PATH"))

    if not discord.opus.is_loaded():
        print(f"Something went wrong loading libopus")
        exit(1)

    asyncio.run(main())
