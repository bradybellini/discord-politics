import httpx
import asyncio
import pandas as pd
from pandas import read_csv
from scripts.webhook_driver import primary_polls_avg_webhook
from scripts.data_parser import primary_avg
from scripts.meta import get_est_time

PRIMARY_POLLS_AVG_LAST_UPDATE = None

STATES = set()

get_state = pd.read_csv(
    'data/primary_average/president_primary_polls_avg.csv', encoding='ANSI')

for i in get_state.state:
    STATES.add(i)


async def fivethirtyeight_primary_polls_avg():
    url = 'https://projects.fivethirtyeight.com/2020-primary-data/pres_primary_avgs_2020.csv'
    headers = {'user-agent': 'Elections 2020 discord bot', 'If-None-Match': ""}
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code, 'avg')
        print(r.headers)
        if r.status_code == 200:
            # with open('data/primary_average/president_primary_polls_avg.csv', 'wb') as f:
            #     f.write(r.content)
            PRIMARY_POLLS_AVG_LAST_UPDATE = await get_est_time()
            # await asyncio.sleep(10)
            # for state in STATES:
            #     await primary_avg(state)
        elif r.status_code != 304:
            await primary_polls_avg_webhook()
        headers = {'user-agent': 'Elections 2020 discord bot',
                   'If-None-Match': r.headers['etag']}
        print(r.headers)
        # print(r.status_code, 'avg')
        # print(PRIMARY_POLLS_AVG_LAST_UPDATE)
        await asyncio.sleep(10)


if __name__ == "__main__":
    current_loops = asyncio.gather(fivethirtyeight_primary_polls_avg())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(current_loops)
