import discord
from discord.ext import commands

class OnlyImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_extensions = {".png", ".jpg", ".jpeg", ".gif"}
        self.image_only_channel = None  # Channel ID for image-only channel

    def is_moderator(self, member):
        # Replace this with your own logic to check if a member is a moderator
        return any(role.name == 'Moderator' for role in member.roles)

    @commands.command(name='onlyimage', aliases=['setimagechannel'])
    @commands.has_permissions(administrator=True)
    async def set_image_channel(self, ctx, channel: discord.TextChannel):
        """
        Set the channel where only images are allowed.
        Usage: .onlyimage <channel_mention>
        """
        self.image_only_channel = channel.id
        await ctx.send(f"Only images are allowed in {channel.mention} now.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is in the configured image-only channel
        if self.image_only_channel and message.channel.id == self.image_only_channel:
            # Check if the author is a moderator
            if self.is_moderator(message.author):
                return  # Moderators can send any messages
            # Check if the message has attachments
            if message.attachments:
                for attachment in message.attachments:
                    # Check if the attachment has an allowed extension
                    if any(attachment.filename.lower().endswith(ext) for ext in self.allowed_extensions):
                        return  # Message has an allowed image attachment, do nothing
                # No valid image attachment found, delete the message
                await message.delete()
                # Send a follow-up message in DM to the user
                await message.author.send("You can only post images in this channel.")
            else:
                # No attachments found, delete the message
                await message.delete()
                # Send a follow-up message in DM to the user
                await message.author.send("You can only post images in this channel.")

def setup(bot):
    bot.add_cog(OnlyImageCog(bot))
