import discord
from redbot.core import commands, Config
import random
import string
import time

class GamblingSystem(commands.Cog):
    """A gambling cog by ze Mx."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)
        self.config.register_user(balance=0, last_daily=0, loan=0, loan_timestamp=0)
        
    @commands.command()
    async def daily(self, ctx):
        """Claim your daily 1000 Generation Wealth"""
        user = ctx.author
        last_claim = await self.config.user(user).last_daily()
        
        if discord.utils.utcnow().timestamp() - last_claim < 86400:
            await ctx.send("You have already claimed your daily reward bitch.")
            return
        
        await self.config.user(user).balance.set(await self.config.user(user).balance() + 1000)
        await self.config.user(user).last_daily.set(discord.utils.utcnow().timestamp())
        await ctx.send("You received 1000 Generation Wealth!")
    
    @commands.command()
    async def mine(self, ctx, amount: int, mines: int):
        """Start a mine game: !mine <amount> <mine_amount>"""
        if mines < 1 or mines > 20:
            await ctx.send("Mine amount must be between 1 and 20.")
            return
        
        user = ctx.author
        balance = await self.config.user(user).balance()
    
        if amount > balance:
            await ctx.send("Bitch you don't have enough Generational Wealth Cuz")
            return
    
        grid_size = 5
        total_cells = grid_size ** 2
        safe_spots = total_cells - mines  
    
        mine_positions = random.sample(range(total_cells), mines)
        revealed = set()
    
        base_multiplier = 1.0 + (mines * 0.05)
        growth_rate = 0.2 + (mines * 0.03)
    
        board = [["⬜" for _ in range(grid_size)] for _ in range(grid_size)]
        alphabet = string.ascii_uppercase[:grid_size]
    
        embed = discord.Embed(title="Mine Game", description=f"You bet {amount} GW. Type a coordinate (e.g., A2)")
        embed.add_field(name="Multiplier", value="0.0x", inline=False)
        embed.set_footer(text="Type !cashout to collect your money hoe")
    
        msg = await ctx.send(embed=embed)
    
        def check(m):
            return m.author == ctx.author and m.content.upper() in [f"{a}{n+1}" for a in alphabet for n in range(grid_size)]
    
        winnings = amount * 0.2
        current_multiplier = 0.2
        playing = True
    
        while playing:
            try:
                guess = await self.bot.wait_for("message", check=check, timeout=30.0)
                coord = guess.content.upper()
                row = alphabet.index(coord[0])
                col = int(coord[1]) - 1
                index = row * grid_size + col
    
                if index in mine_positions:
                    for pos in mine_positions:
                        r, c = divmod(pos, grid_size)
                        board[r][c] = "💣"
                    embed.description = "\n".join([" ".join(row) for row in board])
                    await msg.edit(embed=embed)
                    await ctx.send("💥 You hit a mine! You lost everything.")
                    await self.config.user(user).balance.set(balance - amount)
                    return
    
                revealed.add(index)
                board[row][col] = "💎"
    
                current_multiplier += growth_rate
                winnings = int(amount * current_multiplier)
    
                embed.description = "\n".join([" ".join(row) for row in board])
                embed.set_field_at(0, name="Multiplier", value=f"{current_multiplier:.2f}x", inline=False)
                embed.add_field(name="Potential Winnings", value=f"{winnings} GW", inline=False)
                await msg.edit(embed=embed)
    
            except Exception:
                await ctx.send("Bitch slow ahh grandma be faster next time. Timed Out")
                return
    
        
        @commands.command()
        async def cashout(self, ctx):
            """Cash out winnings."""
            user = ctx.author
            winnings = await self.config.user(user).get_raw("current_winnings", default=0)
            balance = await self.config.user(user).balance()
            
            if winnings <= 0:
                await ctx.send("You have no winnings to cash out.")
                return
            
            await self.config.user(user).balance.set(balance + winnings)
            await self.config.user(user).set_raw("current_winnings", value=0)
            await ctx.send(f"You cashed out with {winnings:.2f} GW!")
    
    @commands.command()
    async def balance(self, ctx):
        """Check yo pocket"""
        user = ctx.author
        balance = await self.config.user(user).balance()
        loan = await self.config.user(user).loan()
        
        if loan > 0:
            debt_display = f"-{loan} Generational Debt"
        else:
            debt_display = "No Debt"
        
        await ctx.send(f"Balance: {balance} GW\nDebt: {debt_display}")
    
    @commands.command()
    async def loan(self, ctx, amount: int):
        """Take a loan (Max 10,000)."""
        user = ctx.author
        loan = await self.config.user(user).loan()
        
        if amount < 1 or loan + amount > 10000:
            await ctx.send("You can only take a loan up to 10,000 GW.")
            return
        
        await self.config.user(user).loan.set(loan + amount)
        await self.config.user(user).balance.set(await self.config.user(user).balance() + amount)
        await self.config.user(user).loan_timestamp.set(time.time())
        await ctx.send(f"You took a loan of {amount} GW. Pay it back to avoid interest!")
    
    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: int):
        """Give someone Generation Wealth."""
        user = ctx.author
        balance = await self.config.user(user).balance()
        
        if amount < 1 or amount > balance:
            await ctx.send("Invalid amount.")
            return
        
        await self.config.user(user).balance.set(balance - amount)
        await self.config.user(member).balance.set(await self.config.user(member).balance() + amount)
        await ctx.send(f"{ctx.author.mention} gave {amount} GW to {member.mention}!")
    
    @commands.command()
    async def repay(self, ctx, amount: int):
        """Repay your loan."""
        user = ctx.author
        balance = await self.config.user(user).balance()
        loan = await self.config.user(user).loan()
        
        if amount < 1 or amount > loan:
            await ctx.send("Invalid repayment amount.")
            return
        
        if amount > balance:
            await ctx.send("You don't have enough GW to repay that.")
            return
        
        await self.config.user(user).balance.set(balance - amount)
        await self.config.user(user).loan.set(loan - amount)
        await ctx.send(f"You repaid {amount} GW. Remaining Generational Debt: {loan - amount} GW")

    @commands.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def hackgw(self, ctx, member: discord.Member, amount: int):
        """Give a user Generational Wealth (Admin Only)"""
        if amount < 1:
            await ctx.send("Bitch you can't hack negative GW.")
            return
        
        new_balance = await self.config.user(member).balance() + amount
        await self.config.user(member).balance.set(new_balance)
        await ctx.send(f"🔥 {ctx.author.mention} just hacked {amount} GW to {member.mention}! 💰")
    
    
    @commands.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def yoinkgw(self, ctx, member: discord.Member, amount: int):
        """Remove Generational Wealth from a user (Admin Only)"""
        balance = await self.config.user(member).balance()
    
        if amount < 1:
            await ctx.send("Bitch you can't yoink negative GW.")
            return
        if amount > balance:
            await ctx.send(f"{member.mention} is already broke. Can't yoink more than what they got.")
            return
    
        new_balance = balance - amount
        await self.config.user(member).balance.set(new_balance)
        await ctx.send(f"🚨 {ctx.author.mention} just yoinked {amount} GW from {member.mention}! 💸")

