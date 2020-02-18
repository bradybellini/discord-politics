import discord
import aiosqlite
from datetime import datetime
from discord.ext import commands


class GuildJoin(commands.Cog, name='Events on Guild Join'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        db = await aiosqlite.connect('main.db')
        cursor = await db.cursor()
        sql = ('SELECT guild_id FROM guilds WHERE guild_id = ?')
        val = (str(ctx.id),)
        await cursor.execute(sql, val)
        results = await cursor.fetchone()
        if not results:
            sql = ('INSERT INTO guilds(guild_id, guild_owner, guild_name, guild_region, guild_boost_count, guild_description, guild_features, in_guild, joined) VALUES(?,?,?,?,?,?,?,?,?)')
            val = (str(ctx.id), str(ctx.owner.id), str(ctx.name),
                   str(ctx.region), int(ctx.premium_subscription_count), str(ctx.description), str(ctx.features), str('true'), int(datetime.utcnow().timestamp()))
            await cursor.execute(sql, val)
            await db.commit()
        else:
            sql = ('UPDATE guilds SET guild_owner = ?, guild_name = ?, guild_region = ?, guild_boost_count = ?, guild_description = ?, guild_features = ?, in_guild = ? WHERE guild_id = ?')
            val = (str(ctx.owner.id), str(ctx.name), str(ctx.region), int(ctx.premium_subscription_count), str(
                ctx.description), str(ctx.features), str('true'), str(ctx.id))
            await cursor.execute(sql, val)
            await db.commit()
        await cursor.close()
        await db.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx):
        db = await aiosqlite.connect('main.db')
        cursor = await db.cursor()
        sql = ('UPDATE guilds SET in_guild = ? WHERE guild_id = ?')
        val = (str('false'), str(ctx.id))
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()


def setup(client):
    client.add_cog(GuildJoin(client))
    print('@EVENT: GuildJoin Event loaded \n---------------------')
