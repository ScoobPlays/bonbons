from disnake.ext.commands import Bot, Cog, Context, command


class Music(Cog, description="Music that makes you feel!"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.player = self.bot.player
        self.emoji = "🎶"

    @command()
    async def join(ctx: Context):
        if ctx.guild.voice_client.is_connected():
            return await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @command()
    async def play(self, ctx: Context, *, url: str):
        player = self.player.get_player(guild_id=ctx.guild.id)
        if not player:
            player = self.player.create_player(ctx, ffmpeg_error_betterfix=True)

        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await ctx.send(f"Playing {song.name}")

        else:
            song = await player.queue(url, search=True)
            await ctx.send(f"Queued {song.name}")

    @command()
    async def pause(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused {song.name}")

    @command()
    async def resume(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed {song.name}")

    @command()
    async def stop(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("Stopped.")

    @command()
    async def loop(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()

        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.name}")

        else:
            await ctx.send(f"Disabled loop for {song.name}")

    @command()
    async def queue(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

    @command()
    async def np(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)

    @command()
    async def skip(self, ctx: Context):
        player = self.player.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)

        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")

        else:
            await ctx.send(f"Skipped {data[0].name}")

    @command()
    async def volume(self, ctx: Context, volume: int):
        player = self.player.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(volume) / 100)
        await ctx.send(f"Changed volume for {song.name} to {int(volume*100)}%.")

    @command()
    async def remove(self, ctx: Context, index: int):
        player = self.player.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed {song.name} from the queue.")


def setup(bot: Bot):
    bot.add_cog(Music(bot))
