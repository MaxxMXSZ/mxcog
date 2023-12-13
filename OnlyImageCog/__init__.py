from .onlyimage import OnlyImageCog

def setup(bot):
    bot.add_cog(OnlyImageCog(bot))