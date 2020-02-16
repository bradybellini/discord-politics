import httpx
import asyncio
import base64
from base64 import b64decode
from apikeys import imgur_client_id
import requests

# On hold. Cannot figure out the path for the picture. Keep getting erros from imgur.

# async def upload_to_imgr():
#     url = 'https://api.imgur.com/3/upload'
#     headers = {'Authorization': f'Client-ID {imgur_client_id}', 'Content-Type': 'image/png' }
#     data = {'image': '@/D:/Documents/Projects/politics-bot/test.png', 'type': 'file'}
#     r = httpx.post(url, headers=headers,data=data)
#     print(r.text.encode('utf-8'))


# # # @/D: / Documents/Projects/politics-bot/test.png

# if __name__ == "__main__":
#     asyncio.run(upload_to_imgr())
