from redbot.core import bot

from .ballsdexvalue import BallsdexValue

async def setup(bot: Red) -> None:
    cog = BallsdexValue(bot)
    await bot.add_cog(cog)
