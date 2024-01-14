from redbot.core import bot

from .ballsdexvalue import BallsdexValue

def setup(bot: bot.Red):
    cog = BallsdexValue(bot)
    bot.add_cog(cog)
