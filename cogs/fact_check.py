import discord
import os
from datetime import datetime
from discord.ext import commands


class FactCheck(commands.Cog, name='Fact Checking related commands'):
    """Fact Checking related commands"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['fc', 'fcheck', 'liedetector', 'pantsonfire'])
    async def factcheck(self, ctx,*, content):
        content_no_spaces = content.replace(" ", "%20")
        check_link = "https://toolbox.google.com/factcheck/explorer/search/" + \
            content_no_spaces + ";hl=en"
        embed = discord.Embed(
            colour=0xfdfdfd)
        embed.set_author(name="Fact Checking via Google Fact Check Tools", url="https://toolbox.google.com/factcheck/explorer/")
        embed.add_field(
            name="**Claim**", value=f"{content}", inline=False)
        embed.add_field(
            name="**Fact Check**", value=f"[Click Here to View]({check_link})", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(
            text="Elections 2020", icon_url=f'{self.client.user.avatar_url}')
        await ctx.send(embed=embed)

        # https://toolbox.google.com/factcheck/explorer/search/Bernie%20Sanders;hl=en


def setup(client):
    client.add_cog(FactCheck(client))
    print('@COG: Fact Check Cog loaded \n---------------------')
