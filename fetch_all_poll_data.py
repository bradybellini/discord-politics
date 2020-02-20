import httpx
import asyncio
import pandas as pd
from pandas import read_csv
from scripts.webhook_driver import fetch_data_webhook
from scripts.data_parser import primary_avg
from datetime import datetime
from pytz import timezone

PRIMARY_POLLS_LAST_UPDATE = None

async def get_est_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    eastern = timezone('US/Eastern')
    est_raw = datetime.now(eastern)
    return est_raw.strftime(fmt)

# not currently using this data
async def fivethirtyeight_primary_polls():
    url = 'https://projects.fivethirtyeight.com/polls-page/president_primary_polls.csv'
    headers = {'user-agent': 'Elections 2020 discord bot',
               'If-None-Match': ""}
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code, 'all')

        if r.status_code == 200:
            with open('data/primary_average/president_primary_polls.csv', 'wb') as f:
                f.write(r.content)
            PRIMARY_POLLS_LAST_UPDATE = await get_est_time()
            await asyncio.sleep(15)
        elif r.status_code != 304:
            # put webhook here
            pass
        else:
            print("success all")

        headers = {'user-agent': 'Elections 2020 discord bot',
                   'If-None-Match': r.headers['etag']}
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code, 'all')
        print(PRIMARY_POLLS_LAST_UPDATE)
        await asyncio.sleep(3600)
