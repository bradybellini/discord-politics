import discord
import os
from datetime import datetime
from discord.ext import commands


class Polls(commands.Cog, name='Poll related commands'):
    """Poll related commands"""

    def __init__(self, client):
        self.client = client
# open file of latest poll
    @commands.group(invoke_without_command=True)
    async def polls(self, ctx):
        ": View the latest polls"
        pass

    @polls.command()
    async def primary(self, ctx, *, state=None):
        ": View the latest polls"
        if state:
            try:
                latest_pic = os.listdir(
                    f'graphs/primary_average_state/{state}/')[-1]
                await ctx.send(content='Type `p.data` to get the raw data.', file=discord.File(f"graphs/primary_average_state/{state}/{latest_pic}"))
            except:
                await ctx.send(f"Either no polls exists for that state(`{state}`) or there is a spelling error.")
        else:
            await ctx.send("Please type in a state to view primary average polls in.")
            

        # embed = discord.Embed(colour=0xb664f8,)

        # embed.set_image(url=discord.File(
        #     f"graphs/primary_average/{latest_pic}"))
        # embed.set_author(name="Latest Democratic Primary Average Polls", url="https://discordapp.com",
        #                 icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        # embed.timestamp = datetime.utcnow()
        # embed.set_footer(
        #     text="Elections 2020", icon_url=f'{self.client.user.avatar_url}')

        # embed.add_field(
        #     name="", value="Link to raw data")

        # await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Polls(client))
    print('@COG: Polls Cog loaded \n---------------------')
