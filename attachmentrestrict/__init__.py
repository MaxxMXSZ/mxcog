from .attachmentrestrict import AttachmentRestrict


async def setup(bot):
    await bot.add_cog(AttachmentRestrict(bot))
