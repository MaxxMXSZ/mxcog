from .gambling import Gambling


async def setup(bot):
    await bot.add_cog(Gambling(bot))
