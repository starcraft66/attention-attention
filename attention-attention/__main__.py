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

import discord
from discord.ext import commands
import aiocron

libopus_loaded = False

try:
    discord.opus._load_default()
    libopus_loaded = True
except OSError as exc:
    print(f"Error loading libopus normally: {exc}")
except AttributeError as exc:
    print(f"Error loading libopus normally: {exc}")

try:
    if not libopus_loaded:
        discord.opus.load_opus(os.getenv("LIBOPUS_PATH"))
except OSError as exc:
    print(f"Error loading libopus from the LIBOPUS_PATH variable: {exc}")
    exit(1)
except AttributeError as exc:
    print(f"Error loading libopus from the LIBOPUS_PATH variable: {exc}")
    exit(1)


def get_media_path(path):
    """
    Unsafely get the path to a resource.
    Using the conext manager allows one to work around
    getting resources from zip files and such, then
    disposing of the termporary files but we don't need
    that and this method will make the code more readable
    """
    with importlib.resources.path(__package__ + ".media", path) as loc:
        return loc


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
            print(anc.audio_file)
            aiocron.crontab(f"{anc.minute} {anc.hour} * * *", func=self.attention, args=[anc.audio_file], start=True)

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


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(command_prefix=commands.when_mentioned_or("!attention"),
                    description="ATTENTION! ATTENTION!",
                    intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} ({bot.user.id})")
        print(f"Discord bot invite link: {discord.utils.oauth_url(client_id=bot.user.id)}")

    token = os.getenv("DISCORD_TOKEN")

    if not token:
        print("DISCORD_TOKEN environment variable is missing!")
        exit()

    bot.add_cog(AttentionAttention(bot))
    bot.run(token)
