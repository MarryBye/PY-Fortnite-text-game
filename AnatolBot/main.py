import discord

from bot_class import CustomBot
from bot_fl_class import GuildFS
from enums_class import GFiles

main_bot = CustomBot(command_prefix='#', intents=discord.Intents.all(), help_command=None)


@main_bot.event
async def on_ready():
    await main_bot.startup_checks()


@main_bot.event
async def on_voice_state_update(member, bef, aft):
    is_join = bef.channel is None
    is_leave = aft.channel is None
    is_move = aft.channel and bef.channel

    if is_join or is_move:
        guild_fs = GuildFS(aft.channel.guild.id)
        guild_settings = guild_fs.load_guild_file(GFiles.GUILD_SETTINGS)

        if aft.channel.id == guild_settings["voice_channel_creator"]:
            voice_channels_table = guild_fs.load_guild_file(GFiles.VOICE_CHANNELS)

            if member.id not in voice_channels_table:
                new_channel = await aft.channel.guild.create_voice_channel(f"Комната {member.name}")
                await member.move_to(new_channel)
                await new_channel.set_permissions(member, manage_channels=True, mute_members=True)

                voice_channels_table[member.id] = new_channel.id
                await guild_fs.save_guild_file(voice_channels_table)

    if is_leave or is_move:
        guild_fs = GuildFS(bef.channel.guild.id)
        voice_channels_table = guild_fs.load_guild_file(GFiles.VOICE_CHANNELS)

        if member not in bef.channel.members:
            if member.id in voice_channels_table:
                if bef.channel.id == voice_channels_table[member.id]:
                    try:
                        channel_to_delete = bef.channel.guild.get_channel(voice_channels_table[member.id])
                        await channel_to_delete.delete()

                        del voice_channels_table[member.id]
                        await guild_fs.save_guild_file(voice_channels_table)
                    except (discord.errors.NotFound, AttributeError):
                        pass


@main_bot.event
async def on_guild_channel_delete(channel):
    entry = [e async for e in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1)]
    guild_fs = GuildFS(channel.guild.id)
    voice_channels_table = guild_fs.load_guild_file(GFiles.VOICE_CHANNELS)
    if entry[0].user.id in voice_channels_table:
        if channel.id == voice_channels_table[entry[0].user.id]:
            del voice_channels_table[entry[0].user.id]
            await guild_fs.save_guild_file(voice_channels_table)


main_bot.run("")
