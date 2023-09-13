import os

from bot_fl_class import GuildFS
from enums_class import GFiles
from discord.ext.commands import Bot


class CustomBot(Bot):

    async def startup_checks(self):

        if not os.path.exists("./data"):
            os.mkdir("data/")

        for guild in self.guilds:
            guild_fs = GuildFS(guild.id)
            if not os.path.exists(guild_fs.guild_folder):
                await guild_fs.create_guild_files()
            voice_channels_to_delete = guild_fs.load_guild_file(GFiles.VOICE_CHANNELS)
            for member in voice_channels_to_delete:
                channel_to_delete = guild.get_channel(voice_channels_to_delete[member])
                if channel_to_delete is not None:
                    await channel_to_delete.delete()
            await guild_fs.save_guild_file({})
