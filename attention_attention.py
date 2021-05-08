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


import discord
import asyncio
import os

from datetime import datetime, timedelta
from discord.ext import commands, tasks

try:
    discord.opus.load_opus("/nix/store/ns50x9ffqqjawgdzpafawwdr69ik8rib-libopus-1.3.1/lib/libopus.so.0")
except:
    print("Error loading libopus from the Nix store")

HOUR = 1
MINUTE = 45

class AttentionAttention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attention.start()
    
    @tasks.loop(hours=24)
    async def attention(self):
        loop = asyncio.get_event_loop()
        vcs_to_play = []
        for guild in self.bot.guilds:
            most_populated_vc = max(guild.voice_channels, key=lambda x: len(x.members))
            if len(most_populated_vc.members) == 0:
                continue
            vcs_to_play.append(most_populated_vc)

        await asyncio.gather(*[self.play_attention_attention(vc) for vc in vcs_to_play])

    async def play_attention_attention(self, voice_channel):
        if voice_channel != None:
            voice_client: discord.VoiceClient = await voice_channel.connect()
            audio_source = discord.FFmpegPCMAudio("ETS_fermeture.mp3")
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()

    @attention.before_loop
    async def before_attention(self):
        await bot.wait_until_ready()
        while True:
            now = datetime.now()
            if now.hour == HOUR and now.minute == MINUTE:
                break
            await asyncio.sleep(45)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description="ATTENTION! ATTENTION!",
                   intents=intents)

@bot.event
async def on_ready():
    print("Logged in as {0} ({0.id})".format(bot.user))
    print(f"Discord bot invite link: {discord.utils.oauth_url(client_id=bot.user.id)}")

token = os.getenv("DISCORD_TOKEN")

if not token:
    print("DISCORD_TOKEN environment variable is missing!")
    exit()

bot.add_cog(AttentionAttention(bot))
bot.run(token)
