import feedparser
import asyncio
import httpx
import aiosqlite
import time
from datetime import datetime

# check etag on this. U think the headers from reuters are not returning fully upon 304 code. Save etag and add logic to check if etag
# exists on the returning header in the loop. 
async def get_reuters():
    url = "http://feeds.reuters.com/Reuters/PoliticsNews"
    headers = {'user-agent': 'Elections 2020 discord bot', 'If-None-Match': ""}
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code)
        print(r.headers)
        if r.status_code == 200:
            print('cool')
            # feed_raw_data = r.text
            # f = feedparser.parse(feed_raw_data)
            # db = await aiosqlite.connect('news.db')
            # cursor = await db.cursor()

            # for entry in f.entries:
            #     guid = entry.guid
            #     title = entry.title
            #     article_url = entry.link
            #     date_published = entry.published
            #     reuters_raw = entry.published_parsed
            #     utc_date = int(time.mktime(reuters_raw))

            #     sql = (
            #         'INSERT INTO all_news(guid, title, article_url, date_published, utc_date) VALUES(?,?,?,?,?)')
            #     val = (guid, title, article_url, date_published, utc_date)
            #     try:
            #         await cursor.execute(sql, val)
            #     except:
            #         pass

            # try:
            #     await db.commit()
            #     await cursor.close()
            #     await db.close()
            # except:
            #     pass
        elif r.status_code != 304:
            await primary_polls_avg_webhook()

        headers = {'user-agent': 'Elections 2020 discord bot',
                'If-None-Match':""}
        await asyncio.sleep(10)
        # f = feedparser.parse(url, etag=if_match)
        # print(f.status)


async def get_pbs():
    url = "https://www.pbs.org/newshour/feeds/rss/politics"
    headers = {'user-agent': 'Elections 2020 discord bot', 'If-None-Match': ""}
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code)
        print(r.headers)
        if r.status_code == 200:
            print('cool')
            # feed_raw_data = r.text
            # f = feedparser.parse(feed_raw_data)
            # db = await aiosqlite.connect('news.db')
            # cursor = await db.cursor()

            # for entry in f.entries:
            #     guid = entry.guid
            #     title = entry.title
            #     article_url = entry.link
            #     date_published = entry.published
            #     reuters_raw = entry.published_parsed
            #     utc_date = int(time.mktime(reuters_raw))

            #     sql = (
            #         'INSERT INTO all_news(guid, title, article_url, date_published, utc_date) VALUES(?,?,?,?,?)')
            #     val = (guid, title, article_url, date_published, utc_date)
            #     try:
            #         await cursor.execute(sql, val)
            #     except:
            #         pass

            # try:
            #     await db.commit()
            #     await cursor.close()
            #     await db.close()
            # except:
            #     pass
        elif r.status_code != 304:
            await primary_polls_avg_webhook()

        headers = {'user-agent': 'Elections 2020 discord bot',
                    'If-None-Match': r.headers['etag']}
        await asyncio.sleep(10)
if __name__ == "__main__":
    current_loops = asyncio.gather(get_reuters())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(current_loops)
