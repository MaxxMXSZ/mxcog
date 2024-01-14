from redbot.core import bot

from .ballsdexvalue import BallsdexValue

async def setup(bot: Red) -> None:
    cog = CodeSnippets(bot)
    await bot.add_cog(cog)
