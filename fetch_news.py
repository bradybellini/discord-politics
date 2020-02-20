import feedparser
import pprint
import asyncio
from datetime import datetime


# try to make it asyn, might have to use something besides feedparser to actually fetch the data and then just use feedparser
# to well parse it lol
async def get_reuters():
    url = "http://feeds.reuters.com/Reuters/PoliticsNews"
    f = feedparser.parse(url)
    print(f.status)
    if_match = f.etag


    f = feedparser.parse(url, etag=if_match)
    print(f.status)
