import feedparser
import pprint
import asyncio
import httpx
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
