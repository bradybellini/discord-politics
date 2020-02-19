import feedparser
import pprint
import asyncio
from datetime import datetime



async def get_reuters():
    url = "http://feeds.reuters.com/Reuters/PoliticsNews"
    f = feedparser.parse(url)
    print(f.status)
    if_match = f.etag


    f = feedparser.parse(url, etag=if_match)
    print(f.status)
