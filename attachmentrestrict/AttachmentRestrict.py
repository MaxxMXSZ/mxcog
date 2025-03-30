from redbot.core import commands, Config, checks
import discord
from datetime import datetime, timedelta
import re

class AttachmentRestrict(commands.Cog):
    """Restricts new members from posting attachments for a set period."""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_guild(enabled=False, wait_time="3d", ignored_channels=[], ignored_roles=[])
    
    @commands.guild_only()
    @commands.admin()
    @commands.group(aliases=["attachrestrict"], invoke_without_command=False)
    async def attachmentrestrict(self, ctx):
        """Manage attachment restrictions for new members."""
    
    @attachmentrestrict.command()
    async def enable(self, ctx, state: bool):
        """Enable or disable attachment restrictions."""
        await self.config.guild(ctx.guild).enabled.set(state)
        status = "enabled" if state else "disabled"
        await ctx.send(f"Attachment restrictions {status}.")
    
    @attachmentrestrict.command()
    async def settime(self, ctx, time: str = None):
        """Set how long new members must wait before posting attachments."""
        if not time:
            await ctx.send("Usage: `.attachmentrestrict settime <time>`\nExample: `.attachmentrestrict settime 3d` (3 days), `.attachmentrestrict settime 2h` (2 hours)")
            return
        
        if not re.match(r"^\d+[dhms]$", time):
            await ctx.send("Invalid format. Use `<number><d/h/m/s>` (e.g., `3d`, `2h`, `1m`, `30s`).")
            return
        
        await self.config.guild(ctx.guild).wait_time.set(time)
        await ctx.send(f"New members must wait `{time}` before posting attachments.")
    
    @attachmentrestrict.group(invoke_without_command=True)
    async def ignore(self, ctx):
        """Ignore a channel or role from attachment restrictions."""
        await ctx.send("Usage: `.attachmentrestrict ignore channel <#channel>` or `.attachmentrestrict ignore role <@role>`.")
    
    @ignore.command(name="channel")
    async def ignore_channel(self, ctx, channel: discord.TextChannel):
        """Ignore a channel from attachment restrictions."""
        async with self.config.guild(ctx.guild).ignored_channels() as ignored:
            if channel.id not in ignored:
                ignored.append(channel.id)
                await ctx.send(f"{channel.mention} will be ignored.")
            else:
                await ctx.send("This channel is already ignored.")
    
    @ignore.command(name="role")
    async def ignore_role(self, ctx, role: discord.Role):
        """Ignore a role from attachment restrictions."""
        async with self.config.guild(ctx.guild).ignored_roles() as ignored:
            if role.id not in ignored:
                ignored.append(role.id)
                await ctx.send(f"{role.mention} will be ignored.")
            else:
                await ctx.send("This role is already ignored.")
    
    @attachmentrestrict.group(invoke_without_command=True)
    async def unignore(self, ctx):
        """Remove a channel or role from the ignore list."""
        await ctx.send("Usage: `.attachmentrestrict unignore channel <#channel>` or `.attachmentrestrict unignore role <@role>`.")
    
    @unignore.command(name="channel")
    async def unignore_channel(self, ctx, channel: discord.TextChannel):
        """Remove a channel from the ignore list."""
        async with self.config.guild(ctx.guild).ignored_channels() as ignored:
            if channel.id in ignored:
                ignored.remove(channel.id)
                await ctx.send(f"{channel.mention} is no longer ignored.")
            else:
                await ctx.send("This channel was not ignored.")
    
    @unignore.command(name="role")
    async def unignore_role(self, ctx, role: discord.Role):
        """Remove a role from the ignore list."""
        async with self.config.guild(ctx.guild).ignored_roles() as ignored:
            if role.id in ignored:
                ignored.remove(role.id)
                await ctx.send(f"{role.mention} is no longer ignored.")
            else:
                await ctx.send("This role was not ignored.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        guild = message.guild
        config = await self.config.guild(guild).all()
        
        if not config["enabled"]:
            return
        
        if message.channel.id in config["ignored_channels"] or any(role.id in config["ignored_roles"] for role in message.author.roles):
            return
        
        account_age = (datetime.utcnow() - message.author.created_at).total_seconds()
        wait_time = self.parse_time(config["wait_time"])
        
        if account_age < wait_time and message.attachments:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you must wait `{config['wait_time']}` before posting attachments.", delete_after=5)
    
    def parse_time(self, time_str):
        unit_multipliers = {"d": 86400, "h": 3600, "m": 60, "s": 1}
        return int(time_str[:-1]) * unit_multipliers[time_str[-1]]
