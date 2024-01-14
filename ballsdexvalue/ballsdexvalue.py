from discord.ext import commands
import math

class BallsdexValue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def clear(self):
        print("\033[H\033[2J")

    def format_modifier(self, modifier):
        is_negative = modifier.startswith("-")
        formatted_string = modifier.replace("+" if modifier.startswith("+") else "-", "").replace("%", "")
        return -int(formatted_string) if is_negative else int(formatted_string)

    @commands.command(name="ballsdexvalue")
    async def balls_dex_value(self, ctx):
        print("Enter rarity to calculate (If you want to see how many top ones you can get, put 1)")
        raritycalc = int(input())

        self.clear()

        print("Enter rarity")
        rankstat = int(input())

        self.clear()

        if rankstat == 0:
            print("You must enter a valid number.")
            return

        print("Enter attack modifier (EX: +20%)")
        attack_input = input()

        attackstat = 0

        if "%" in attack_input:
            attackstat = self.format_modifier(attack_input)
        else:
            attackstat = int(attack_input)

        self.clear()

        print("Enter health modifier (EX: +20%)")
        health_input = input()

        healthstat = 0

        if "%" in health_input:
            healthstat = self.format_modifier(health_input)
        else:
            healthstat = int(health_input)

        self.clear()

        print("Enter shiny (true or false)")
        ifshiny = input().lower() == "true"

        self.clear()

        print("Enter event. (coming soon, enter random integer)")
        whichevent = int(input())

        self.clear()

        totalstats = 0
        multiplier = 200 if ifshiny else 1

        totalstats = healthstat + attackstat
        rankval = 1000 / rankstat

        if totalstats >= 10:
            multiplier += 0.1
        if totalstats >= 20:
            multiplier += 0.1
        if totalstats >= 30:
            multiplier += 0.3
        if totalstats >= 38:
            multiplier += 0.5
        if totalstats >= 39:
            multiplier += 3
        if totalstats >= 40:
            multiplier += ((50 / rankstat) + 10) * ((rankval * 2) / 125)
        if totalstats <= -10:
            multiplier -= 0.05
        if totalstats <= -20:
            multiplier -= 0.1
        if totalstats <= -30:
            multiplier -= 0.2
        if totalstats <= -40:
            multiplier += 5.5

        finalval = round((((((1000 / rankstat) - 8) + (2600 / rankstat)) / 2) * multiplier)) * 10
        tx = round((((1000 / raritycalc) - 8) + (2600 / raritycalc) / 2) * 10)
        finalvalabove8 = round(((1000 / rankstat) * multiplier)) * 10
        txabove8 = round((1000 / raritycalc) * 10)
        result = round((finalval / tx) * 10)
        result2 = round((finalval / txabove8) * 10)
        resultabove8 = round((finalvalabove8 / txabove8) * 10)
        resultabove82 = round((finalvalabove8 / tx) * 10)

        if rankstat != 8 and rankstat != 1:
            print(finalval / 10)
        else:
            print(finalvalabove8 / 10)

        if (raritycalc != 8 and raritycalc != 1) and ((rankstat != 8 and rankstat != 1)):
            print(f"(a score of {tx / 10} is equal to 1 T{raritycalc} ball)")
            print(f"this ball is worth about {resultabove8 / 10} T{raritycalc}'s")
        elif (raritycalc != 8 and raritycalc != 1) and ((rankstat == 8 or rankstat == 1)):
            print(f"(a score of {tx / 10} is equal to 1 T{raritycalc} ball)")
            print(f"this ball is worth about {resultabove82 / 10} T{raritycalc}'s")
        elif rankstat != 8 and rankstat != 1:
            print(f"(a score of {txabove8 / 10} is equal to 1 T{raritycalc} ball)")
            print(f"this ball is worth about {result2 / 10} T{raritycalc}'s")
        else:
            print(f"(a score of {txabove8 / 10} is equal to 1 T{raritycalc} ball)")
            print(f"this ball is worth about {result / 10} T{raritycalc}'s")

        print("Keep in mind that this calculator is still under development. Calculations are likely to be off just a little bit.")
