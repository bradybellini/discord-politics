import httpx
import asyncio
import pandas as pd
from pandas import read_csv
from scripts.webhook_driver import fetch_data_webhook
from scripts.data_parser import primary_avg
from datetime import datetime
from pytz import timezone

# @TODO: make it more efficient to grab all relevant data from 538. Think about passing in url string to the function from the various files that get updated.
# The abive might not work as I will need to keep track of the etag and I would have to restart the loop everytime it changed?
# I could use something like cron and have the script run every so often to check, but doing everything nateivly seems more efficient at the moment
# send error to email or something when you get certain status codes

# send a webhook to a channel when polls are updated

PRIMARY_POLLS_LAST_UPDATE = None
PRIMARY_POLLS_AVG_LAST_UPDATE = None

STATES = set()

get_state = pd.read_csv(
    'data/primary_average/president_primary_polls_avg.csv', encoding='ANSI')

for i in get_state.state:
    STATES.add(i)

async def driver():
    await asyncio.gather(fivethirtyeight_primary_polls_avg())


async def get_est_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    eastern = timezone('US/Eastern')
    est_raw = datetime.now(eastern)
    return est_raw.strftime(fmt)


async def get_phx_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    phx = timezone('America/Phoenix')
    est_raw = datetime.now(phx)
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


async def fivethirtyeight_primary_polls_avg():
    url = 'https://projects.fivethirtyeight.com/2020-primary-data/pres_primary_avgs_2020.csv'
    headers = {'user-agent': 'Elections 2020 discord bot',
               'If-None-Match': ""}
    while True:
        # get initial etag
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code, 'avg')
        # check status from etag
        if r.status_code == 200:
            # download csv file and save it
            with open('data/primary_average/president_primary_polls_avg.csv', 'wb') as f:
                f.write(r.content)
            PRIMARY_POLLS_AVG_LAST_UPDATE = await get_est_time()
            # a little sleep to make sure everthing propagates? its just like a safety net to make sure everthing is good before
            # rendering all of the graphs
            await asyncio.sleep(15)
            # creates all of the graphs from the data downloaded. gets states from global.
            for state in STATES:
                await primary_avg(state)
        # if something besides 304 or 200 happen sends a message to a webhook in discord letting me know @TODO
        elif r.status_code != 304:
            # put webhook here
            pass
        else:
            send_error = f"There has been an error in the loop where the status code is {r.status_code}"
            send_location = "fetch_data.py in function fivethirtyeight_primary_polls_avg"
        # adds log input that everything is good @TODO
            await fetch_data_webhook(send_error, send_location, await get_phx_time())
        # another request to get the etag. after the loop runs thru once, that is when it checks for etag.
        headers = {'user-agent': 'Elections 2020 discord bot',
                'If-None-Match': r.headers['etag']}
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
        print(r.status_code, 'avg')
        print(PRIMARY_POLLS_AVG_LAST_UPDATE)
        await asyncio.sleep(10)


if __name__ == "__main__":
    current_loops = asyncio.gather(fivethirtyeight_primary_polls_avg(), fivethirtyeight_primary_polls())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(current_loops)

