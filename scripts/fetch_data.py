import httpx
import urllib
import asyncio
from data_parser import primary_avg
from datetime import datetime
from pytz import timezone

# @TODO: make it more efficient to grab all relevant data from 538. Think about passing in url string to the function from the various files that get updated.
# The abive might not work as I will need to keep track of the etag and I would have to restart the loop everytime it changed?
# I could use something like cron and have the script run every so often to check, but doing everything nateivly seems more efficient at the moment
# send error to email or something when you get certain status codes
# send a webhook to a channel when polls are updated
PRIMARY_POLLS_LAST_UPDATE = None
PRIMARY_POLLS_AVG_LAST_UPDATE = None


async def driver():
    await asyncio.gather(fivethirtyeight_primary_polls(), fivethirtyeight_primary_polls_avg())


def get_est_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    eastern = timezone('US/Eastern')
    est_raw = datetime.now(eastern)
    return est_raw.strftime(fmt)


async def fivethirtyeight_primary_polls():
    url = 'https://projects.fivethirtyeight.com/polls-page/president_primary_polls.csv'
    headers = {'user-agent': 'Elections 2020 discord bot',
               'If-None-Match': ""}
    while True:
        r = httpx.get(url, headers=headers)
        print(r.status_code, 'main')

        if r.status_code == 200:
            with urllib.request.urlopen(url) as primary_polls, open('data/primary_general_state/president_primary_polls.csv', 'w') as f:
                f.write(primary_polls.read().decode())
            PRIMARY_POLLS_LAST_UPDATE = get_est_time()
        else:
            pass

        headers = {'user-agent': 'Elections 2020 discord bot',
                   'If-None-Match': r.headers['etag']}
        r = httpx.get(url, headers=headers)
        print(r.status_code, 'main')
        print(PRIMARY_POLLS_LAST_UPDATE)
        await asyncio.sleep(900)
    print('loop broke')
    # put in webhook to channel if loop breaks

async def fivethirtyeight_primary_polls_avg():
    url = 'https://projects.fivethirtyeight.com/2020-primary-data/pres_primary_avgs_2020.csv'
    headers = {'user-agent': 'Elections 2020 discord bot',
               'If-None-Match': ""}
    while True:

        r = httpx.get(url, headers=headers)
        print(r.status_code, 'avg')

        if r.status_code == 200:
            with urllib.request.urlopen(url) as primary_polls_avg, open('data/primary_average/president_primary_polls_avg.csv', 'w') as f:
                f.write(primary_polls_avg.read().decode())
            PRIMARY_POLLS_AVG_LAST_UPDATE = get_est_time()
            # await asyncio.sleep(15)
            # await primary_avg()
        else:
            pass

        headers = {'user-agent': 'Elections 2020 discord bot',
                   'If-None-Match': r.headers['etag']}
        r = httpx.get(url, headers=headers)
        print(r.status_code, 'avg')
        print(PRIMARY_POLLS_AVG_LAST_UPDATE)
        await asyncio.sleep(900)


if __name__ == "__main__":
    asyncio.run(driver())
