import httpx
import asyncio
from datetime import datetime
from pytz import timezone


def get_phx_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    phx = timezone('America/Phoenix')
    est_raw = datetime.now(phx)
    return est_raw.strftime(fmt)

async def fetch_data_webhook(error, location, time):
    data_template = {
        "embeds": [
            {
                "title": f"ERROR",
                "description": "this is the description",
                "color": 16711680,
                "fields": [
                    {
                        "name": "Time of Incident",
                        "value": f"{time}"
                    },
                    {
                        "name": "Location of incident",
                        "value": f"{location}"
                    },
                    {
                        "name": "What Happened?",
                        "value": f"{error}"
                    }
                ],
                "timestamp": f"{get_phx_time()}"
            }
        ]
    }
    webhook_url = "https://discordapp.com/api/webhooks/679441151014600719/uU1BZBKX5QYb_vjpDLG8A1XWddXIZjN16cg_x2A1JhD-ub_RsfcrQopK5LiCGoz03NZ_"
    async with httpx.AsyncClient() as client:
        await client.put(webhook_url, data=data_template)


if __name__ == "__main__":
    send_error = f"There has been an error in the loop where the status code is 404"
    send_location = "fetch_data.py in function fivethirtyeight_primary_polls_avg"
    time = get_phx_time()
    asyncio.run(fetch_data_webhook(send_error, send_location, time))
 
