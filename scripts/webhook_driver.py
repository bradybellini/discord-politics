import httpx
import asyncio


async def primary_polls_avg_webhook():
    webhook_url = "https://discordapp.com/api/webhooks/679441151014600719/uU1BZBKX5QYb_vjpDLG8A1XWddXIZjN16cg_x2A1JhD-ub_RsfcrQopK5LiCGoz03NZ_"
    payload = "{\r\n  \"embeds\": [\r\n    {\r\n      \"title\": \"There has been an error.\",\r\n      \"description\": \"There has been an error in the fivethirtyeight_primary_polls_avg() loop regarding the status of the FiveThirtyEight website.\",\r\n      \"color\": 16711680\r\n    }\r\n  ]\r\n}"
    headers = {'Content-Type': 'application/json'}
    client = httpx.AsyncClient()
    await client.post(webhook_url, data=payload, headers=headers)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(primary_polls_avg_webhook())

