from .gamblingsystem import GamblingSystem.py


async def setup(bot):
    await bot.add_cog(GamblingSystem(bot))
