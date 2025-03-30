from .attachmentrestrict import attachmentrestrict


async def setup(bot):
    await bot.add_cog(attachmentrestrict(bot))
