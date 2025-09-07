import discord
from discord.ext import commands
import yt_dlp
import asyncio
from bot.utils import load_config

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        self.config = load_config()
        text_channel_id = self.config.get("TEXT_CHANNEL_ID")
        voice_channel_id = self.config.get("VOICE_CHANNEL_ID")

        if not text_channel_id or not voice_channel_id:
            return

        if message.channel.id != int(text_channel_id):
            return

        # Simple check for youtube url
        if 'youtube.com/watch' in message.content or 'youtu.be/' in message.content:
            voice_channel = self.bot.get_channel(int(voice_channel_id))
            if not voice_channel:
                await message.channel.send("Configured voice channel not found.")
                return

            # Connect to voice channel if not already connected
            if not message.guild.voice_client:
                await voice_channel.connect()
            elif message.guild.voice_client.channel != voice_channel:
                await message.guild.voice_client.move_to(voice_channel)

            await self.play_song(message, message.content)

    async def play_song(self, ctx, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        if ctx.guild.voice_client.is_playing():
             ctx.guild.voice_client.stop()

        async with ctx.channel.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                await ctx.channel.send(f'Now playing: {player.title}')
                ctx.guild.voice_client.source.volume = self.config.get("VOLUME", 0.5)

            except Exception as e:
                await ctx.channel.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Music(bot))
