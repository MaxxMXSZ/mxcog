import discord

from .ballsdexvalue import BallsdexValue

from redbot.core.bot import Red


async def setup(bot: Red):
    await bot.add_cog(BallsdexValue(bot))
