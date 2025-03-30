from redbot.core import commands, Config, checks
import discord
from datetime import datetime, timedelta

class AttachmentRestrict(commands.Cog):
    """Restricts new members from posting attachments for a set period."""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_guild(enabled=False, wait_days=3, ignored_channels=[])
    
    @commands.guild_only()
    @commands.admin()
    @commands.group()
    async def attachrestrict(self, ctx):
        """Manage attachment restrictions for new members."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()
    
    @attachrestrict.command()
    async def enable(self, ctx):
        """Enable attachment restrictions."""
        await self.config.guild(ctx.guild).enabled.set(True)
        await ctx.send("Attachment restrictions enabled.")
    
    @attachrestrict.command()
    async def disable(self, ctx):
        """Disable attachment restrictions."""
        await self.config.guild(ctx.guild).enabled.set(False)
        await ctx.send("Attachment restrictions disabled.")
    
    @attachrestrict.command()
    async def setdays(self, ctx, days: int):
        """Set the number of days a user must wait before posting attachments."""
        if days < 0:
            return await ctx.send("Number of days must be at least 0.")
        await self.config.guild(ctx.guild).wait_days.set(days)
        await ctx.send(f"New members must wait {days} day(s) before posting attachments.")
    
    @attachrestrict.command()
    async def ignore(self, ctx, channel: discord.TextChannel):
        """Ignore a channel from attachment restrictions."""
        async with self.config.guild(ctx.guild).ignored_channels() as ignored:
            if channel.id not in ignored:
                ignored.append(channel.id)
                await ctx.send(f"{channel.mention} will be ignored.")
            else:
                await ctx.send("This channel is already ignored.")
    
    @attachrestrict.command()
    async def unignore(self, ctx, channel: discord.TextChannel):
        """Remove a channel from the ignore list."""
        async with self.config.guild(ctx.guild).ignored_channels() as ignored:
            if channel.id in ignored:
                ignored.remove(channel.id)
                await ctx.send(f"{channel.mention} is no longer ignored.")
            else:
                await ctx.send("This channel was not ignored.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        guild = message.guild
        config = await self.config.guild(guild).all()
        
        if not config["enabled"]:
            return
        
        if message.channel.id in config["ignored_channels"]:
            return
        
        account_age = (datetime.utcnow() - message.author.created_at).days
        if account_age < config["wait_days"] and message.attachments:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you must wait {config['wait_days']} day(s) before posting attachments.", delete_after=5)

async def setup(bot):
    bot.add_cog(AttachmentRestrict(bot))
