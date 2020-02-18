import discord
import os
from datetime import datetime
from discord.ext import commands


class Polls(commands.Cog, name='Poll related commands'):
    """Poll related commands"""

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, aliases=['poll', 'p'])
    async def polls(self, ctx):
        ": View the latest polls"
        embed = discord.Embed(
            colour=0xfdfdfd, description="[] = required argument \n<> = optional argument ",)
        embed.set_author(name="Available Polls and Commands")
        embed.add_field(
            name="Democratic Primary", value=f"`p.polls [primary|demprimary|democraticprimary] [state]`", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(
            text="Elections 2020", icon_url=f'{self.client.user.avatar_url}')
        await ctx.send(embed=embed)

    @polls.command(aliases=['demprimary', 'democraticprimary'])
    async def primary(self, ctx, *, state):
        ": View the latest polls"
        try:
            latest_pic = os.listdir(
                f'graphs/primary_average_state/{state}/')[-1]
            file = discord.File(
                f"graphs/primary_average_state/{state}/{latest_pic}", filename=latest_pic)
            embed = discord.Embed(
                colour=0xfdfdfd, description="[Data Source](https://projects.fivethirtyeight.com/2020-primary-data/pres_primary_avgs_2020.csv)")
            embed.set_image(url=f"attachment://{latest_pic}")
            embed.set_author(name="Latest Democratic Primary Average Polls")
            embed.timestamp = datetime.utcnow()
            embed.set_footer(
                text="Elections 2020", icon_url=f'{self.client.user.avatar_url}')
            await ctx.send(file=file, embed=embed)
        except:
            embed = discord.Embed(
                title="Either no polls exists for that state or there is a spelling error.\nTry: p.polls primary [state]", colour=0xd95454)
            embed.set_author(name=f"Something went wrong...")
            await ctx.send(embed=embed)

    @primary.error
    async def new_ticket_error(self, ctx, error):
        embed = discord.Embed(
            title="Try: p.polls primary [state]", colour=0xd95454)
        embed.set_author(name=f"{error}")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f" Try again in {int(error.retry_after)//60} minutes.", colour=0xd95454)
            cooldown_embed.set_author(
                name=f"You are on a cooldown for this command!")
            await ctx.send(embed=cooldown_embed)


def setup(client):
    client.add_cog(Polls(client))
    print('@COG: Polls Cog loaded \n---------------------')
