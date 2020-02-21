import feedparser
import asyncio
import httpx
import aiosqlite
from datetime import datetime


# try to make it asyn, might have to use something besides feedparser to actually fetch the data and then just use feedparser
# to well parse it lol
async def get_reuters():
    url = "http://feeds.reuters.com/Reuters/PoliticsNews"
    headers = {'user-agent': 'Elections 2020 discord bot', 'If-None-Match': ""}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
    # print(r.headers)
    feed_raw_data = r.text
    f = feedparser.parse(feed_raw_data)
    # f.entries[1].pprint
    db = await aiosqlite.connect('news.db')
    cursor = await db.cursor()
    for entry in f.entries:
        guid = entry.guid
        title = entry.title
        # published = need to convert this to est time why is time and date so hard to deal with fuck
        article_url = entry.link
        sql = ('SELECT guild_id FROM guilds WHERE guild_id = ?')
        val = (str(ctx.id),)
        try:
            await cursor.execute(sql, val)
        except aiosqlite.Error as error:
            print(f"There was an Error: {error}")
    print(f.entries[1]['guid']) 
    print(f.entries[1]['title'])
    print(f.entries[1]['published'])
    print(f.entries[1]['link'])
    # f = feedparser.parse(url, etag=if_match)
    # print(f.status)
if __name__ == "__main__":
    current_loops = asyncio.gather(get_reuters())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(current_loops)
