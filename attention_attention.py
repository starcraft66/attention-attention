import discord
import asyncio
import os

from discord.ext import commands

try:
    discord.opus.load_opus("/nix/store/ns50x9ffqqjawgdzpafawwdr69ik8rib-libopus-1.3.1/lib/libopus.so.0")
except:
    print("Error loading libopus from the Nix store")

class AttentionAttention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def attention(self, ctx):
        user = ctx.author
        voice_channel=user.voice.channel
        if voice_channel != None:
            voice_client: discord.VoiceClient = await voice_channel.connect()
            audio_source = discord.FFmpegPCMAudio("ETS_fermeture.mp3")
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description="ATTENTION! ATTENTION!")

@bot.event
async def on_ready():
    print("Logged in as {0} ({0.id})".format(bot.user))

token = os.getenv("DISCORD_TOKEN")

if not token:
    print("DISCORD_TOKEN environment variable is missing!")
    exit()

bot.add_cog(AttentionAttention(bot))
bot.run(os.getenv("DISCORD_TOKEN"))