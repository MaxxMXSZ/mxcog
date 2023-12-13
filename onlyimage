import discord
from redbot.core import commands

class AutoDeleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  # Set this to the desired channel ID

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is from the specified channel
        if message.channel.id == self.channel_id:
            try:
                # Delete the message
                await message.delete()
            except discord.Forbidden:
                # Bot doesn't have permission to delete messages
                pass

def setup(bot):
    bot.add_cog(AutoDeleteCog(bot))
