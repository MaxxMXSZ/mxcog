from .GamblingSystem import GamblingSystem


async def setup(bot):
    await bot.add_cog(GamblingSystem(bot))
