import discord
import os
from datetime import datetime
from discord.ext import commands


class Data(commands.Cog, name='Data related commands'):
    """Data related commands"""

    def __init__(self, client):
        self.client = client


    @commands.group(invoke_without_command=True)
    async def data(self, ctx):
        ": View main data menu"
        embed = discord.Embed(
            colour=0xfdfdfd)
        embed.set_author(name="Data Sources for Polling Graphs")
        embed.add_field(
            name="**Democratic Primary Data**", value=f"Source: FiveThirtyEight \nRaw Data: [Click here to view](https://projects.fivethirtyeight.com/polls-page/president_primary_polls.csv)", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(
            text="Elections 2020", icon_url=f'{self.client.user.avatar_url}')
        await ctx.send(embed=embed)


    @data.command()
    async def polls(self, ctx):
        ": View main data menu"
        # make embed to send it in to shorten link or just make one bif embed with all poll data
        await ctx.send('https://projects.fivethirtyeight.com/polls-page/president_primary_polls.csv')


    

def setup(client):
    client.add_cog(Data(client))
    print('@COG: Data Cog loaded \n---------------------')
